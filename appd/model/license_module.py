"""
Model classes for AppDynamics REST API
"""

from . import JsonObject, JsonList


class LicenseModule(JsonObject):

    FIELDS = {'name': ''}

    def __init__(self, name=None):
        self.name = name


class LicenseModuleList(JsonList):
    """
    Represents a collection of :class:Account objects. Extends :class:UserList, so it supports the
    standard array index and :keyword:`for` semantics.
    """
    def __init__(self, initial_list=None):
        super(LicenseModuleList, self).__init__(LicenseModule, initial_list)

    def __getitem__(self, i):
        """
        :rtype: LicenseModule
        """
        return self.data[i]

    def by_name(self, name):
        """
        Finds an account by name.

        :returns: First account with the correct name
        :rtype: LicenseModule
        """
        found = [x for x in self.data if x.name == name]
        try:
            return found[0]
        except IndexError:
            raise KeyError(name)

    def __contains__(self, item):
        found = [x for x in self.data if x.name == item]
        return True if found else False


class LicenseModules(JsonObject):

    FIELDS = {}

    def __init__(self):
        self.modules = LicenseModuleList()

    @classmethod
    def from_json(cls, json_dict):
        obj = super(LicenseModules, cls).from_json(json_dict)
        obj.modules = LicenseModuleList.from_json(json_dict['modules'])
        return obj

