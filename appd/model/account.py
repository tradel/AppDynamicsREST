"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList


class Account(JsonObject):
    """
    Represents a tenant account on the controller. The following attributes are defined:

    .. data:: id

        Numeric ID of the account.

    .. data:: name

        Account name.
    """

    FIELDS = {'id': '', 'name': ''}

    def __init__(self, acct_id='0', name=None):
        self.id, self.name = acct_id, name


class Accounts(JsonList):
    """
    Represents a collection of :class:Account objects. Extends :class:UserList, so it supports the
    standard array index and :keyword:`for` semantics.
    """
    def __init__(self, initial_list=None):
        super(Accounts, self).__init__(Account, initial_list)

    def __getitem__(self, i):
        """
        :rtype: Account
        """
        return self.data[i]

    def by_name(self, name):
        """
        Finds an account by name.

        :returns: First account with the correct name
        :rtype: Account
        """
        found = [x for x in self.data if x.name == name]
        try:
            return found[0]
        except IndexError:
            raise KeyError(name)
