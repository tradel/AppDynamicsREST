"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList
from appd.time import from_ts


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
        for k, v in list(Snapshot.FIELDS.items()):
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

    def __getitem__(self, i):
        """
        :rtype: Snapshot
        """
        return self.data[i]
