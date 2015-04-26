"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from . import JsonObject, JsonList
from appd.time import from_ts

class MetricValue(JsonObject):

    FIELDS = {
        'current': '',
        'min': '',
        'max': '',
        'value': '',
        'start_time_ms': 'startTimeInMillis'
    }

    def __init__(self, current=0, value=0, min_value=0, max_value=0, start_time_ms=0):
        (self.current, self.value, self.min, self.max, self.start_time_ms) = (current, value, min_value, max_value,
                                                                              start_time_ms)

    @property
    def start_time(self):
        """
        Gets the timestamp of the metric data, converting it from an AppDynamics timestamp to standard
        Python :class:`datetime`.

        :return: Time the violation was resolved
        :rtype: :class:`datetime.datetime`
        """
        return from_ts(self.start_time_ms)


class MetricValues(JsonList):

    def __init__(self, initial_list=None):
        super(MetricValues, self).__init__(MetricValue, initial_list)

    def __getitem__(self, i):
        """
        :rtype: MetricValue
        """
        return self.data[i]
