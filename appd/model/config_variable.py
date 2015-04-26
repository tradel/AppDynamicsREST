"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList


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

    def __getitem__(self, i):
        """
        :rtype: ConfigVariable
        """
        return self.data[i]

    def by_name(self, name):
        """
        Finds a config variable with the matching name.

        :param str name: Variable name to find.
        :return: The matching config variable.
        :rtype: appd.model.ConfigVariable
        """
        found = [x for x in self.data if x.name == name]
        try:
            return found[0]
        except IndexError:
            raise KeyError(name)
