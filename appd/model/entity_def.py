"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList


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
