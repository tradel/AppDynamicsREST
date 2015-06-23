#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from collections import OrderedDict

import pygal
import tzlocal

from appd.request import AppDynamicsClient
import creds.demo2 as creds

__author__ = 'Todd Radel'
__copyright__ = 'Copyright (c) 2013-2015 AppDynamics Inc.'
__version__ = '0.4.3'

# Set up API client
c = AppDynamicsClient(creds.url, creds.user, creds.password, creds.account)

# Get my tenant account info
my_acct = c.get_my_account()

# Calculate start and end dates - we will start at midnight last night and go back 7 days
days = 15
mytz = tzlocal.get_localzone()
end_dt = datetime.now(mytz).replace(hour=0, minute=0, second=0, microsecond=0)
start_dt = end_dt - timedelta(days)

# Get license usage for my account
usage = c.get_license_usage(my_acct.id, 'java', start_dt, end_dt)


def daterange(start_dt, end_dt):
    for n in range(int((end_dt - start_dt).days)):
        yield start_dt + timedelta(days=n)


usage_by_day = OrderedDict()
for day in daterange(start_dt, end_dt):
    units = [x.max_units_used for x in usage.usages if x.created_on.date() == day.date()]
    usage_by_day[day] = max(units)

# Make a simple graph and display it
chart = pygal.StackedBar(x_label_rotation=45, width=1000)
chart.title = 'Java License Usage - ' + c.base_url
chart.x_labels = [str(x.date()) for x in daterange(start_dt, end_dt)]
chart.add('java', usage_by_day.values())
chart.render_to_file('java_usage.svg')
