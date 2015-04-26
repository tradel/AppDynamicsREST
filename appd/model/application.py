"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList


class Application(JsonObject):
    """
    Represents a business application. The following attributes are defined:

    .. data:: id

        Numeric ID of the application.

    .. data:: name

        Application name.

    .. data:: description

        Optional description of the application.
    """

    FIELDS = {'id': '', 'name': '', 'description': ''}

    def __init__(self, app_id=0, name=None, description=None):
        self.id, self.name, self.description = app_id, name, description


class Applications(JsonList):
    """
    Represents a collection of :class:`Application` objects. Extends :class:`UserList`, so it supports the
    standard array index and :keyword:`for` semantics.
    """
    def __init__(self, initial_list=None):
        super(Applications, self).__init__(Application, initial_list)

    def __getitem__(self, i):
        """
        :rtype: Application
        """
        return self.data[i]

    def by_name(self, name):
        """
        Finds an application by name.

        :returns: First application with the correct name
        :rtype: :class:`Application`
        """
        found = [x for x in self.data if x.name == name]
        try:
            return found[0]
        except IndexError:
            raise KeyError(name)
