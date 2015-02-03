__author__ = 'Todd Radel <tradel@appdynamics.com>'

import sys
import requests
from model import *


class AppDynamicsClient(object):

    TIME_RANGE_TYPES = ('BEFORE_NOW', 'BEFORE_TIME', 'AFTER_TIME', 'BETWEEN_TIMES')

    DEEP_DIVE_POLICIES = ('SLA_FAILURE', 'TIME_SAMPLING', 'ERROR_SAMPLING', 'OCCURRENCE_SAMPLING',
                          'ON_DEMAND', 'HOTSPOT', 'HOTSPOT_LEARN', 'APPLICATION_STARTUP', 'DIAGNOSTIC_SESSION',
                          'SLOW_DIAGNOSTIC_SESSION', 'ERROR_DIAGNOSTIC_SESSION', 'POLICY_FAILURE_DIAGNOSTIC_SESSION',
                          'INFLIGHT_SLOW_SESSION')

    USER_EXPERIENCES = ('NORMAL', 'SLOW', 'VERY_SLOW', 'STALL', 'BUSINESS_ERROR')

    COLLECTOR_TYPES = ('ERROR_IDS', 'STACK_TRACES', 'ERROR_DETAIL', 'HTTP_PARAMETER', 'BUSINESS_DATA',
                       'COOKIE', 'HTTP_HEADER', 'SESSION_KEY', 'RESPONSE_HEADER', 'LOG_MESSAGE',
                       'TRANSACTION_PROPERTY', 'TRANSACTION_EVENT', 'DOTNET_PROPS', 'DOTNET_SET')

    SNAPSHOT_REQUEST_PARAMS = ('guids', 'archived', 'deep-dive-policy', 'application-component-ids',
                               'application-component-node-ids', 'business-transaction-ids', 'user-experience',
                               'first-in-chain', 'need-props', 'need-exit-calls', 'execution-time-in-millis',
                               'session-id', 'user-principal-id', 'error-ids', 'error-occurred',
                               'bad-request', 'diagnostic-snapshot', 'diagnostic-session-guid',
                               'starting-request-id', 'ending-request-id',
                               'data-collector-name', 'data-collector-type', 'data-collector-value')

    SNAPSHOT_REQUEST_LISTS = ('business-transaction-ids', 'user-experience', 'error-ids', 'guids', 'deep-dive-policy',
                              'application-component-ids', 'application-component-node-ids', 'diagnostic-session-guid')

    CPM = CALLS_PER_MINUTE = 'Calls per Minute'
    ART = AVERAGE_RESPONSE_TIME = 'Average Response Time (ms)'
    NORMAL_ART = 'Normal Average Response Time (ms)'
    SLOW_CALLS = 'Number of Slow Calls'
    VERY_SLOW_CALLS = 'Number of Very Slow Calls'
    EPM = ERRORS_PER_MINUTE = 'Errors per Minute'
    EXCEPTIONS_PER_MINUTE = 'Exceptions per Minute'
    STALLS = 'Stall Count'


    def __init__(self, base_url='http://localhost:8090', username='user1', password='welcome',
                 account='customer1', debug=False):
        self._username, self._password, self._account, self._app_id = '', '', '', None
        (self.base_url, self.username, self.password, self.account, self.debug) = (base_url, username, password,
                                                                                   account, debug)

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, new_url):
        self._base_url = new_url
        if not '://' in self._base_url:
            self._base_url = 'http://' + self._base_url
        while self._base_url.endswith('/'):
            self._base_url = self._base_url[:-1]
        self._base_url += '/controller/rest'

    def __make_auth(self):
        self._auth = (self._username+'@'+self._account, self._password)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, new_username):
        self._username = new_username
        self.__make_auth()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        self._password = new_password
        self.__make_auth()

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, new_account):
        self._account = new_account
        self.__make_auth()

    @property
    def app_id(self):
        return self._app_id

    @app_id.setter
    def app_id(self, new_app_id):
        self._app_id = new_app_id

       def request(self, path, params=None, method='GET', json=True):
        if not path.startswith('/'):
            path = '/' + path
        url = self._base_url + path

        params = params or {}
        if json:
            params['output'] = 'JSON'
        for k in params.keys():
            if params[k] is None:
                del params[k]
                
        if self.debug:
            print 'Retrieving ' + url, self._auth, params
            
        r = requests.request(method ,url, auth=self._auth, params=params)
        
        if r.status_code != requests.codes.ok:
            print >>sys.stderr, url
            r.raise_for_status()
        if(json):
            return r.json()
        return r.text

    def _app_path(self, app_id, path=None):
        id = app_id if isinstance(app_id, int) else self._app_id
        if not id:
            raise ValueError('application id is required')
        path = '/applications/%s' % id + (path or '')
        return path

    def get_metric_tree(self, app_id=None, metric_path=None, recurse=False):
        parent = None
        if metric_path:
            parent = MetricTreeNode(parent=None, node_name=metric_path, node_type='folder')
        return self.__get_metric_tree(app_id, parent=parent, recurse=recurse)

    def __get_metric_tree(self, app_id=None, parent=None, recurse=False):
        params = {}
        if parent:
            params['metric-path'] = parent.path
        path = '/applications/%d/metrics' % app_id
        nodes = MetricTreeNodes.from_json(self.request(path, params), parent)
        if recurse:
            for node in nodes:
                if node.type == 'folder':
                    self.__get_metric_tree(app_id, parent=node, recurse=True)
        return nodes

    # Top-level requests

    def _top_request(self, cls, path):
        return cls.from_json(self.request(path))

    def get_config(self):
        return self._top_request(ConfigVariables, '/configuration')

    def get_applications(self):
        return self._top_request(Applications, '/applications')

    # Application-level requests

    def _app_request(self, cls, path, app_id=None, params=None):
        path = self._app_path(app_id, path)
        return cls.from_json(self.request(path, params))

    def get_bt_list(self, app_id=None):
        return self._app_request(BusinessTransactions, '/business-transactions', app_id)

    def get_tiers(self, app_id=None):
        return self._app_request(Tiers, '/tiers', app_id)

    def get_nodes(self, app_id=None, tier_id=None):
        """
        Returns the list of nodes in the application, optionally filtered by tier.
        """
        path = ('/tiers/%s/nodes' % tier_id) if tier_id else '/nodes'
        return self._app_request(Nodes, path, app_id)

    def _validate_time_range(self, time_range_type, duration_in_mins, start_time, end_time):

        if time_range_type and not time_range_type in self.TIME_RANGE_TYPES:
            raise ValueError('time_range_time must be one of: ' + ', '.join(self.TIME_RANGE_TYPES))

        elif time_range_type == 'BEFORE_NOW' and not duration_in_mins:
            raise ValueError('when using BEFORE_NOW, you must specify duration_in_mins')

        elif time_range_type == 'BEFORE_TIME' and (not end_time or not duration_in_mins):
            raise ValueError('when using BEFORE_TIME, you must specify duration_in_mins and end_time')

        elif time_range_type == 'AFTER_TIME' and (not start_time or not duration_in_mins):
            raise ValueError('when using AFTER_TIME, you must specify duration_in_mins and start_time')

        elif time_range_type == 'BETWEEN_TIMES' and (not start_time or not end_time):
            raise ValueError('when using BETWEEN_TIMES, you must specify start_time and end_time')

        return {'time-range-type': time_range_type,
                'duration-in-mins': duration_in_mins,
                'start-time': start_time,
                'end-time': end_time}

    def get_metrics(self, metric_path, app_id=None, time_range_type='BEFORE_NOW',
                    duration_in_mins=15, start_time=None, end_time=None, rollup=True):

        params = self._validate_time_range(time_range_type, duration_in_mins, start_time, end_time)
        params.update({'metric-path': metric_path,
                       'rollup': rollup})

        return self._app_request(MetricData, '/metric-data', app_id, params)

    def get_snapshots(self, app_id=None, time_range_type=None, duration_in_mins=None,
                      start_time=None, end_time=None, **kwargs):

        self._validate_time_range(time_range_type, duration_in_mins, start_time, end_time)

        params = self._validate_time_range(time_range_type, duration_in_mins, start_time, end_time)

        for qs_name in self.SNAPSHOT_REQUEST_PARAMS:
            arg_name = qs_name.replace('-', '_')
            params[qs_name] = kwargs.get(arg_name, None)
            if qs_name in self.SNAPSHOT_REQUEST_LISTS and kwargs.has_key(qs_name):
                params[qs_name] = ','.join(params[qs_name])

        return self._app_request(Snapshots, '/request-snapshots', app_id, params)

    def get_policy_violations(self, app_id=None, time_range_type='BEFORE_NOW', duration_in_mins=15,
                              start_time=None, end_time=None):

        params = self._validate_time_range(time_range_type, duration_in_mins, start_time, end_time)

        return self._app_request(PolicyViolations, '/problems/policy-violations', app_id, params)

