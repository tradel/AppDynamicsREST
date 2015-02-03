"""
This module contains the main classes for handling requests to the AppDynamics REST API.

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

from __future__ import absolute_import

from datetime import datetime
from time import mktime


def from_ts(ms):
    """
    Converts a timestamp from AppDynamics internal format to a Python :class:`datetime <datetime.datetime>` object.

    :param ms: Timestamp expressed as milliseconds since epoch.
    :return: Converted value.
    :rtype: :class:`datetime <datetime.datetime>`
    """

    return datetime.fromtimestamp(ms / 1000)


def to_ts(dt):
    """
    Converts a timestamp from Python :class:`datetime <datetime.datetime>` to AppDynamics format.

    :param dt: Timestamp expressed as a :class:`datetime <datetime.datetime>`.
    :return: Converted value.
    :rtype: long
    """

    return long(mktime(dt.timetuple())) * 1000


