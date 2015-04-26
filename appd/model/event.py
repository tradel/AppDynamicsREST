"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList
from .entity_def import EntityDefinition

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
        """
        :return:
        """
        return self._event_type

    @event_type.setter
    def event_type(self, new_type):
        self._list_setter('_event_type', new_type, Event.EVENT_TYPES)


class Events(JsonList):

    def __init__(self, initial_list=None):
        super(Events, self).__init__(Event, initial_list)

    def __getitem__(self, i):
        """
        :rtype: Event
        """
        return self.data[i]
