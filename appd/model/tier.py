"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList


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
        """
        :rtype: str
        """
        return self._agent_type

    @agent_type.setter
    def agent_type(self, agent_type):
        self._list_setter('_agent_type', agent_type, Tier.AGENT_TYPES)


class Tiers(JsonList):

    def __init__(self, initial_list=None):
        super(Tiers, self).__init__(Tier, initial_list)

    def __getitem__(self, i):
        """
        :rtype: Tier
        """
        return self.data[i]

    def by_agent_type(self, agent_type):
        """
        Searches for tiers of a particular type (which should be one of Tier.AGENT_TYPES). For example, to find
        all the Java app server tiers:

        >>> from appd.request import AppDynamicsClient
        >>> client = AppDynamicsClient(...)
        >>> all_tiers = client.get_tiers()
        >>> java_tiers = all_tiers.by_agent_type('APP_AGENT')

        :returns: a Tiers object containing any tiers matching the criteria
        :rtype: Tiers
        """
        return Tiers([x for x in self.data if x.agentType == agent_type])
