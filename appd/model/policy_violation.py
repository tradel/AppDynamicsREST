"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList
from .entity_def import EntityDefinition
from appd.time import from_ts


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
        """
        Gets the end time of the violation, converting it from an AppDynamics timestamp to standard
        Python :class:datetime.

        :return: Time the violation was resolved
        :rtype: datetime
        """
        return from_ts(self.end_time_ms)

    @property
    def detected_time(self):
        return from_ts(self.detected_time_ms)


class PolicyViolations(JsonList):

    def __init__(self, initial_list=None):
        super(PolicyViolations, self).__init__(PolicyViolation, initial_list)

    def __getitem__(self, i):
        """
        :rtype: PolicyViolation
        """
        return self.data[i]
