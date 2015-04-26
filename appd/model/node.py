"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList


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

    def __getitem__(self, i):
        """
        :rtype: Node
        """
        return self.data[i]

    def by_machine_name(self, name):
        """
        Filters a Nodes collection to return only the nodes matching the given hostname.
        :param str name: Hostname to match against.
        :returns: a Nodes collection filtered by hostname.
        :rtype: Nodes
        """
        return Nodes([x for x in self.data if x.machineName == name])

    def by_machine_id(self, machine_id):
        """
        Filters a Nodes collection to return only the nodes matching the given machine instance ID.
        :param int machine_id: Machine ID to match against.
        :returns: a Nodes collection filtered by machine ID.
        :rtype: Nodes
        """
        return Nodes([x for x in self.data if x.machineId == machine_id])

    def by_tier_name(self, name):
        """
        Filters a Nodes collection to return only the nodes belonging to the given tier.
        :param str name: Tier name to match against.
        :returns: a Nodes collection filtered by tier.
        :rtype: Nodes
        """
        return Nodes([x for x in self.data if x.tier_name == name])

    def by_tier_id(self, tier_id):
        """
        Filters a Nodes collection to return only the nodes belonging to the given tier ID.
        :param int tier_id: Tier ID to match against.
        :returns: a Nodes collection filtered by tier.
        :rtype: Nodes
        """
        return Nodes([x for x in self.data if x.tier_id == tier_id])
