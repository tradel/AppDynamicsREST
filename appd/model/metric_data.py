"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList
from .metric_value import MetricValues

class MetricDataSingle(JsonObject):

    FIELDS = {
        'frequency': '',
        'path': 'metricPath'
    }

    FREQUENCIES = ('ONE_MIN', 'TEN_MIN', 'SIXTY_MIN')

    def __init__(self, path='', frequency='ONE_MIN', values=MetricValues()):
        self._frequency = None
        self.path, self.frequency, self.values = path, frequency, values

    @classmethod
    def _set_fields_from_json_dict(cls, obj, json_dict):
        JsonObject._set_fields_from_json_dict(obj, json_dict)
        obj.values = MetricValues.from_json(json_dict['metricValues'])

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, new_freq):
        self._list_setter('_frequency', new_freq, MetricDataSingle.FREQUENCIES)


class MetricData(JsonList):
    def __init__(self, initial_list=None):
        super(MetricData, self).__init__(MetricDataSingle, initial_list)

    def __getitem__(self, i):
        """
        :rtype: MetricDataSingle
        """
        return self.data[i]

    def by_partial_name(self, name):
        return MetricData([x for x in self if name in x.path])

    def by_leaf_name(self, name):
        return MetricData([x for x in self if x.path.split('|')[-1] == name])

    def by_path(self, path):
        return MetricData([x for x in self if x.path == path])

    def first_value(self):
        return self[0].values[0].value
