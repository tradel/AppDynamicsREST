"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""


from six.moves import UserList
from appd.time import from_ts
from datetime import datetime


def _filter_func(obj, pred):
    def func():
        return obj.__class__([item for item in obj.data])

    return func


class JsonObject(object):

    FIELDS = {}

    @classmethod
    def _set_fields_from_json_dict(cls, obj, json_dict):
        for k, v in list(obj.FIELDS.items()):
            obj.__setattr__(k, json_dict[v or k])

    @classmethod
    def from_json(cls, json_dict):
        obj = cls()
        cls._set_fields_from_json_dict(obj, json_dict)
        return obj

    def __str__(self):
        rep = ', '.join([x + '=' + repr(y) for x, y in list(self.__dict__.items())])
        return '<{0}: {1}>'.format(self.__class__.__name__, rep)

    __repr__ = __str__

    def _list_setter(self, attr_name, new_val, allowed_vals):
        if new_val and (new_val not in allowed_vals):
            raise ValueError('{0} must be one of [{1}] but got {2}'.format(
                attr_name, ', '.join(allowed_vals), new_val))
        self.__setattr__(attr_name, new_val)


class JsonList(UserList):

    OBJECT_TYPE = None

    def __init__(self, cls, initial_list=None):
        UserList.__init__(self)
        if initial_list:
            for item in initial_list:
                if isinstance(item, cls):
                    self.data.append(item)
                elif isinstance(item, dict):
                    self.data.append(cls.from_json(item))

    @classmethod
    def from_json(cls, json_list):
        return cls(json_list)

    def __str__(self):
        rep = ', '.join([str(x) for x in self.data])
        return '<{0}[{1}]: {2}>'.format(self.__class__.__name__, len(self.data), rep)

