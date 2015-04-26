"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList


class BusinessTransaction(JsonObject):
    """
    Represents a business transaction definition.

    .. data:: id

        Numeric ID of the BT definition.

    .. data:: name

    """
    FIELDS = {'id': '', 'name': '', 'type': 'entryPointType', 'internal_name': 'internalName',
              'is_background': 'background', 'tier_id': 'tierId', 'tier_name': 'tierName'}

    def __init__(self, bt_id=0, name='', internal_name='', tier_id=0, tier_name='',
                 bt_type='POJO', is_background=False):
        (self.id, self.name, self.internal_name, self.tier_id, self.tier_name, self.type, self.is_background) = \
            (bt_id, name, internal_name, tier_id, tier_name, bt_type, is_background)


class BusinessTransactions(JsonList):

    def __init__(self, initial_list=None):
        super(BusinessTransactions, self).__init__(BusinessTransaction, initial_list)

    def __getitem__(self, i):
        """
        :rtype: BusinessTransaction
        """
        return self.data[i]

    def by_name(self, bt_name):
        """
        Searches for business transactions that match a particular name. Note that there may be more than one
        exact match, as different tiers can have transactions with the exact same name.

        :returns: a BusinessTransactions object containing the matching business transactions.
        :rtype: BusinessTransactions
        """
        return BusinessTransactions([x for x in self.data if x.name == bt_name])

    def by_tier_and_name(self, bt_name, tier_name):
        """
        Searches for business transactions that match a particular BT name and tier name.

        :returns: a BusinessTransactions object containing the matching business transactions.
        :rtype: BusinessTransactions
        """
        return BusinessTransactions([x for x in self.data if x.name == bt_name and x.tier_name == tier_name])


