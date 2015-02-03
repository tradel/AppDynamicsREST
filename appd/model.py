"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

__author__ = 'Todd Radel'


from UserList import UserList
from string import Template
from .time import from_ts

def _filter_func(obj, pred):
    def func():
        return obj.__class__([item for item in obj.data])
    return func


class JsonObject(object):
    FIELDS = {}

    @classmethod
    def _set_fields_from_json_dict(cls, obj, json_dict):
        for k, v in obj.FIELDS.items():
            obj.__setattr__(k, json_dict[v or k])

    @classmethod
    def from_json(cls, json_dict):
        obj = cls()
        cls._set_fields_from_json_dict(obj, json_dict)
        return obj

    def __str__(self):
        lrepr = ', '.join([x + '=' + repr(y) for x, y in self.__dict__.items()])
        return Template("<$cls: $lrepr>").substitute(cls=self.__class__.__name__, lrepr=lrepr)

    __repr__ = __str__

    def _list_setter(self, attr_name, new_val, allowed_vals):
        if new_val and (new_val not in allowed_vals):
            raise ValueError("event_type must be one of " + ', '.join(allowed_vals) + " but got " + new_val)
        self.__setattr__(attr_name, new_val)


class JsonList(UserList):
    OBJECT_TYPE = None

    def __init__(self, cls, initial_list=None):
        UserList.__init__(self)
        if initial_list:
            for item in initial_list:
                if isinstance(item, cls):
                    self.data.append(item)
                elif isinstance(item, dict):
                    self.data.append(cls.from_json(item))

    @classmethod
    def from_json(cls, json_list):
        return cls(json_list)

    def __str__(self):
        lrepr = ', '.join([str(x) for x in self.data])
        return Template("<$cls[$len]: $lrepr>").substitute(cls=self.__class__.__name__,
                                                           len=len(self.data), lrepr=lrepr)


class Application(JsonObject):
    """
    Represents a business application. The following attributes are defined:

    .. data:: id

        Numeric ID of the application.

    .. data:: name

        Application name.

    .. data:: description

        Optional description of the application.
    """

    FIELDS = {'id': '', 'name': '', 'description': ''}

    def __init__(self, app_id=0, name=None, description=None):
        self.id, self.name, self.description = app_id, name, description


class Applications(JsonList):
    """
    Represents a collection of :class:`Application` objects. Extends :class:`UserList`, so it supports the
    standard array index and :keyword:`for` semantics.
    """

    def __init__(self, initial_list=None):
        super(Applications, self).__init__(Application, initial_list)

    def by_name(self, n):
        found = [x for x in self.data if x.name == n]
        try:
            return found[0]
        except IndexError:
            raise KeyError(n)


class BusinessTransaction(JsonObject):
    FIELDS = {'id': '', 'name': '', 'type': 'entryPointType', 'internal_name': 'internalName',
              'is_background': 'background', 'tier_id': 'tierId', 'tier_name': 'tierName'}

    def __init__(self, bt_id=0, name='', internal_name='', tier_id=0, tier_name='',
                 bt_type='POJO', is_background=False):
        (self.id, self.name, self.internal_name, self.tier_id, self.tier_name, self.type, self.is_background) = \
            (bt_id, name, internal_name, tier_id, tier_name, bt_type, is_background)


class BusinessTransactions(JsonList):
    def __init__(self, initial_list=None):
        super(BusinessTransactions, self).__init__(BusinessTransaction, initial_list)

    def by_name(self, bt_name):
        return BusinessTransactions([x for x in self.data if x.name == bt_name])

    def by_tier_and_name(self, bt_name, tier_name):
        return BusinessTransactions([x for x in self.data if x.name == bt_name and x.tier_name == tier_name])


class Tier(JsonObject):
    FIELDS = {'id': '', 'name': '', 'description': '', 'type': '',
              'node_count': 'numberOfNodes', 'agent_type': 'agentType'}
    AGENT_TYPES = ('APP_AGENT', 'MACHINE_AGENT',
                   'DOT_NET_APP_AGENT', 'DOT_NET_MACHINE_AGENT',
                   'PHP_APP_AGENT', 'PHP_MACHINE_AGENT')

    def __init(self, tier_id=0, name='', description='', agent_type='JAVA_AGENT', node_count=0,
               tier_type='Java Application Server'):
        self._agent_type = None
        self.id, self.name, self.description, self.agent_type, self.node_count, self.type = \
            tier_id, name, description, agent_type, node_count, tier_type

    @property
    def agent_type(self):
        return self._agent_type

    @agent_type.setter
    def agent_type(self, agent_type):
        self._list_setter('_agent_type', agent_type, Tier.AGENT_TYPES)


class Tiers(JsonList):
    def __init__(self, initial_list=None):
        super(Tiers, self).__init__(Tier, initial_list)

    def by_agent_type(self, agent_type):
        return Tiers([x for x in self.data if x.agentType == agent_type])


class Node(JsonObject):
    FIELDS = {'id': '', 'name': '', 'type': '', 'machine_id': 'machineId', 'machine_name': 'machineName',
              'tier_id': 'tierId', 'tier_name': 'tierName', 'unique_id': 'nodeUniqueLocalId',
              'os_type': 'machineOSType', 'has_app_agent': 'appAgentPresent', 'app_agent_version': 'appAgentVersion',
              'has_machine_agent': 'machineAgentPresent', 'machine_agent_version': 'machineAgentVersion'}

    def __init__(self, node_id=0, name='', node_type='', machine_id=0, machine_name='', os_type='',
                 unique_local_id='', tier_id=0, tier_name='', has_app_agent=False, app_agent_version='',
                 has_machine_agent=False, machine_agent_version=''):
        (self.id, self.name, self.type, self.machine_id, self.machine_name, self.os_type, self.unique_local_id,
         self.tier_id, self.tier_name, self.has_app_agent, self.app_agent_version, self.has_machine_agent,
         self.machine_agent_version) = (node_id, name, node_type, machine_id, machine_name, os_type, unique_local_id,
                                        tier_id, tier_name, has_app_agent, app_agent_version,
                                        has_machine_agent, machine_agent_version)


class Nodes(JsonList):
    def __init__(self, initial_list=None):
        super(Nodes, self).__init__(Node, initial_list)

    def by_machine_name(self, name):
        return Nodes([x for x in self.data if x.machineName == name])

    def by_machine_id(self, machine_id):
        return Nodes([x for x in self.data if x.machineId == machine_id])

    def by_tier_name(self, name):
        return Nodes([x for x in self.data if x.tierName == name])

    def by_tier_id(self, tier_id):
        return Nodes([x for x in self.data if x.tierId == tier_id])


class MetricValue(JsonObject):
    FIELDS = {
        'current': '',
        'min': '',
        'max': '',
        'value': '',
        'start_time_ms': 'startTimeInMillis'
    }

    def __init__(self, current=0, value=0, min_value=0, max_value=0, start_time_ms=0):
        (self.current, self.value, self.min, self.max, self.start_time_ms) = (current, value, min_value, max_value,
                                                                              start_time_ms)

    @property
    def start_time(self):
        return from_ts(self.start_time_ms)


class MetricValues(JsonList):
    def __init__(self, initial_list=None):
        super(MetricValues, self).__init__(MetricValue, initial_list)


class MetricDataSingle(JsonObject):
    FIELDS = {
        'frequency': '',
        'path': 'metricPath'
    }

    FREQUENCIES = ('ONE_MIN', 'TEN_MIN', 'SIXTY_MIN')

    def __init__(self, path='', frequency='ONE_MIN', values=MetricValues()):
        self._frequency = None
        self.path, self.frequency, self.values = path, frequency, values

    @classmethod
    def _set_fields_from_json_dict(cls, obj, json_dict):
        JsonObject._set_fields_from_json_dict(obj, json_dict)
        obj.values = MetricValues.from_json(json_dict['metricValues'])

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, new_freq):
        self._list_setter('_frequency', new_freq, MetricDataSingle.FREQUENCIES)


class MetricData(JsonList):
    def __init__(self, initial_list=None):
        super(MetricData, self).__init__(MetricDataSingle, initial_list)

    def by_partial_name(self, name):
        return MetricData([x for x in self if name in x.path])

    def by_leaf_name(self, name):
        return MetricData([x for x in self if x.path.split('|')[-1] == name])

    def by_path(self, path):
        return MetricData([x for x in self if x.path == path])

    def first_value(self):
        return self[0].values[0].value


class Snapshot(JsonObject):
    FIELDS = {'id': '', 'local_id': 'localID', 'request_guid': 'requestGUID', 'summary': '',
              'bt_id': 'businessTransactionId', 'app_id': 'applicationId',
              'url': 'URL', 'archived': '', 'async': '', 'stall_dump': 'stallDump',
              'call_chain': 'callChain', 'is_first_in_chain': 'firstInChain',
              'diag_session_guid': 'diagnosticSessionGUID', 'exit_sequence': 'snapshotExitSequence',
              'exit_calls_truncated': 'exitCallsDataTruncated',
              'exit_calls_truncated_msg': 'exitCallsDataTruncationMessage',
              'app_component_id': 'applicationComponentId', 'app_component_node_id': 'applicationComponentNodeId',
              'local_start_time_ms': 'localStartTime', 'server_start_time_ms': 'serverStartTime',
              'thread_id': 'threadID', 'thread_name': 'threadName',
              'http_headers': 'httpHeaders', 'response_headers': 'responseHeaders',
              'http_params': 'httpParameters', 'cookies': '',
              'http_session_id': 'httpSessionID', 'session_keys': 'sessionKeys', 'business_data': 'businessData',
              'error_ids': 'errorIDs', 'error_occurred': 'errorOccured', 'error_summary': 'errorSummary',
              'error_details': 'errorDetails', 'log_messages': 'logMessages',
              'bt_events': 'transactionEvents', 'bt_properties': 'transactionProperties',
              'dotnet_properties': 'dotnetProperty',
              'has_deep_dive_data': 'hasDeepDiveData', 'deep_dive_policy': 'deepDivePolicy',
              'is_delayed_deep_dive': 'delayedDeepDive', 'delayed_deep_dive_offset': 'delayedDeepDiveOffSet',
              'has_unresolved_calls': 'unresolvedCallInCallChain',
              'time_taken_ms': 'timeTakenInMilliSecs', 'cpu_time_taken_ms': 'cpuTimeTakenInMilliSecs',
              'warning_threshold': 'warningThreshold', 'critical_threshold': 'criticalThreshold',
              'user_experience': 'userExperience'}

    def __init__(self, snap_id=0, **kwargs):
        self.id = snap_id
        self.local_start_time_ms, self.server_start_time_ms = 0, 0
        for k, v in Snapshot.FIELDS.items():
            self.__setattr__(k, kwargs.get(k, None))

    @property
    def local_start_time(self):
        return from_ts(self.local_start_time_ms)

    @property
    def server_start_time(self):
        return from_ts(self.server_start_time_ms)


class Snapshots(JsonList):
    def __init__(self, initial_list=None):
        super(Snapshots, self).__init__(Snapshot, initial_list)


class ConfigVariable(JsonObject):
    """
    Represents a controller configuration variable. The following attributes are defined:

    .. data:: name

       Variable name.

    .. data:: value

      Current value.

    .. data:: description

      Optional description of the variable.

    .. data:: updateable

      If :const:`True`, value can be changed.

    .. data:: scope

      Scope of the variable. The scope can be ``'cluster'`` or ``'local'``. Variables with cluster scope are
      replicated across HA controllers; local variables are not.
    """

    FIELDS = {
        'name': '',
        'description': '',
        'scope': '',
        'updateable': '',
        'value': ''
    }

    def __init__(self, name='', description='', scope='cluster', updateable=True, value=None):
        (self.name, self.description, self.scope, self.updateable, self.value) = (name, description, scope,
                                                                                  updateable, value)


class ConfigVariables(JsonList):
    """
    Represents a collection of :class:`ConfigVariable` objects. Extends :class:`UserList`, so it supports the
    standard array index and :keyword:`for` semantics.
    """

    def __init__(self, initial_list=None):
        super(ConfigVariables, self).__init__(ConfigVariable, initial_list)


class MetricTreeNode(JsonObject):
    FIELDS = {'name': '', 'type': ''}
    NODE_TYPES = ('leaf', 'folder')

    def __init__(self, parent=None, node_name='', node_type=''):
        self.parent, self.name, self.type = parent, node_name, node_type
        self._children = MetricTreeNodes()
        if parent:
            parent._children.append(self)

    @property
    def path(self):
        n = self
        stack = []
        while n:
            stack.insert(0, n.name)
            n = n.parent
        return '|'.join(stack)


class MetricTreeNodes(JsonList):
    def __init__(self, initial_list=None, parent=None):
        super(MetricTreeNodes, self).__init__(MetricTreeNode, initial_list)

        self.parent = parent
        if parent:
            if not isinstance(parent, MetricTreeNode):
                raise TypeError('was expecting a MetricTreeNode')
            for x in self.data:
                x.parent = parent

    @classmethod
    def from_json(cls, json_list, parent=None):
        return cls(json_list, parent)

    def by_name(self, n):
        found = [x for x in self.data if x.name == n]
        try:
            return found[0]
        except IndexError:
            raise KeyError(n)


class EntityDefinition(JsonObject):
    FIELDS = {'entity_id': 'entityId',
              'type': 'entityType'}

    ENTITY_TYPES = ('ACCOUNT', 'AGENT_CONFIGURATION', 'ALL', 'APPLICATION', 'APPLICATION_COMPONENT',
                    'APPLICATION_COMPONENT_NODE', 'APPLICATION_DIAGNOSTIC_DATA', 'AUTOMATIC_LEAK_DETECTION',
                    'BACKEND', 'BACKEND_DISCOVERY_CONFIG', 'BUSINESS_TRANSACTION', 'BUSINESS_TRANSACTION_GROUP',
                    'CALL_GRAPH_CONFIGURATION', 'CUSTOM_EXIT_POINT_DEFINITION', 'CUSTOM_MATCH_POINT_DEFINITION',
                    'CUSTOM_MEMORY_STRUCTURE', 'DASHBOARD', 'ERROR', 'ERROR_CONFIGURATION',
                    'DOT_NET_ERROR_CONFIGURATION', 'PHP_ERROR_CONFIGURATION', 'EUM_CONFIGURATION', 'EVENT',
                    'GLOBAL_CONFIGURATION', 'INCIDENT', 'JMX_CONFIG', 'MACHINE_INSTANCE', 'MEMORY_CONFIGURATION',
                    'NOTIFICATION_CONFIG', 'OBJECT_INSTANCE_TRACKING', 'POLICY', 'RULE', 'SQL_DATA_GATHERER_CONFIG',
                    'STACK_TRACE', 'THREAD_TASK', 'TRANSACTION_MATCH_POINT_CONFIG', 'USER', 'GROUP', 'ACCOUNT_ROLE',
                    'WORKFLOW', 'WORKFLOW_EXCUTION', 'POJO_DATA_GATHERER_CONFIG', 'HTTP_REQUEST_DATA_GATHERER_CONFIG',
                    'BASE_PAGE', 'IFRAME', 'AJAX_REQUEST')

    def __init__(self, entity_id=0, entity_type=''):
        self._type = None
        (self.id, self.type) = (entity_id, entity_type)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        self._list_setter('_type', new_type, EntityDefinition.ENTITY_TYPES)


class PolicyViolation(JsonObject):
    FIELDS = {'id': '',
              'name': '',
              'description': '',
              'status': 'incidentStatus',
              'severity': '',
              'start_time_ms': 'startTimeInMillis',
              'end_time_ms': 'endTimeInMillis',
              'detected_time_ms': 'detectedTimeInMillis',
              'deep_link_url': 'deepLinkUrl'}

    STATUSES = ('NOT_APPLICABLE', 'OPEN', 'RESOLVED')

    SEVERITIES = ('INFO', 'WARNING', 'CRITICAL')

    def __init__(self, pv_id=0, pv_name='', description='', status='OPEN', severity='INFO',
                 start_time_ms=0, end_time_ms=0, detected_time_ms=0, deep_link_url='',
                 affected_entity=None, triggered_entity=None):
        self._severity = None
        self._status = None
        (self.id, self.name, self.description, self.status, self.severity, self.start_time_ms, self.end_time_ms,
         self.detected_time_ms, self.deep_link_url, self.affected_entity, self.triggered_entity) = \
            (pv_id, pv_name, description, status, severity, start_time_ms, end_time_ms, detected_time_ms,
             deep_link_url, affected_entity, triggered_entity)

    @classmethod
    def _set_fields_from_json_dict(cls, obj, json_dict):
        JsonObject._set_fields_from_json_dict(obj, json_dict)
        obj.affected_entity = EntityDefinition.from_json(json_dict['affectedEntityDefinition'])
        obj.triggered_entity = EntityDefinition.from_json(json_dict['triggeredEntityDefinition'])

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self._list_setter('_status', new_status, PolicyViolation.STATUSES)

    @property
    def severity(self):
        return self._severity

    @severity.setter
    def severity(self, new_sev):
        self._list_setter('_severity', new_sev, PolicyViolation.SEVERITIES)

    @property
    def start_time(self):
        return from_ts(self.start_time_ms)

    @property
    def end_time(self):
        return from_ts(self.end_time_ms)

    @property
    def detected_time(self):
        return from_ts(self.detected_time_ms)


class Event(JsonObject):
    FIELDS = {'id': '',
              'summary': '',
              'type': '',
              'archived': '',
              'deep_link_url': 'deepLinkUrl',
              'event_time_ms': 'eventTime',
              'is_read': 'markedAsRead',
              'is_resolved': 'markedAsResolved',
              'severity': '',
              'sub_type': 'subType'}

    EVENT_TYPES = ('APPLICATION_ERROR', 'STALL', 'DEADLOCK', 'MEMORY_LEAK', 'MEMORY_LEAK_DIAGNOSTICS',
                   'LOW_HEAP_MEMORY', 'CUSTOM', 'APP_SERVER_RESTART', 'SYSTEM_LOG', 'INFO_INSTRUMENTATION_VISIBILITY',
                   'AGENT_EVENT', 'AGENT_STATUS', 'ACTIVITY_TRACE', 'OBJECT_CONTENT_SUMMARY', 'DIAGNOSTIC_SESSION',
                   'HIGH_END_TO_END_LATENCY', 'APPLICATION_CONFIG_CHANGE', 'APPLICATION_DEPLOYMENT',
                   'AGENT_DIAGNOSTICS', 'MEMORY', 'LICENSE', 'CONTROLLER_AGENT_VERSION_INCOMPATIBILITY', 'DISK_SPACE',
                   'APPDYNAMICS_DATA', 'APPDYNAMICS_CONFIGURATION_WARNINGS', 'POLICY_OPEN', 'POLICY_CLOSE',
                   'POLICY_UPGRADED', 'POLICY_DOWNGRADED', 'RESOURCE_POOL_LIMIT')

    def __init__(self, event_id=0, event_type='CUSTOM', sub_type='', summary='', archived=False, event_time_ms=0,
                 is_read=False, is_resolved=False, severity='INFO', deep_link_url='',
                 triggered_entity=None, affected_entities=None):
        self._event_type = None
        (self.id, self.type, self.sub_type, self.summary, self.archived, self.event_time_ms, self.is_read,
         self.is_resolved, self.severity, self.deep_link_url) = (event_id, event_type, sub_type, summary, archived,
                                                                 event_time_ms, is_read, is_resolved, severity,
                                                                 deep_link_url)
        self.triggered_entity = triggered_entity or EntityDefinition()
        self.affected_entities = affected_entities or []

    @property
    def event_type(self):
        return self._event_type

    @event_type.setter
    def event_type(self, new_type):
        self._list_setter('_event_type', new_type, Event.EVENT_TYPES)


class PolicyViolations(JsonList):
    def __init__(self, initial_list=None):
        super(PolicyViolations, self).__init__(PolicyViolation, initial_list)
