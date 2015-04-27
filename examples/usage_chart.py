#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from datetime import datetime, timedelta

import pandas as pd
import pylab
import tzlocal

from appd.request import AppDynamicsClient
import creds.oa as creds

__author__ = 'Todd Radel'
__copyright__ = 'Copyright (c) 2013-2015 AppDynamics Inc.'
__version__ = '0.4.1'

# Set up API clientgit
c = AppDynamicsClient(creds.url, creds.user, creds.password, creds.account)

# Get my tenant account info
my_acct = c.get_my_account()

# Calculate start and end dates - we will start at midnight last night and go back 7 days
mytz = tzlocal.get_localzone()
midnight = datetime.now(mytz).replace(hour=0, minute=0, second=0, microsecond=0)
end_dt = midnight - timedelta(hours=1)
start_dt = midnight - timedelta(days=7)

# Get license usage for my account
usage = c.get_license_usage(my_acct.id, 'java', start_dt, end_dt)

# Make a simple graph and display it
series = pd.Series([x.max_units_used for x in usage.usages], index=[x.created_on for x in usage.usages])
plot = series.plot(title='Java License Usage - 1 Week')
pylab.show()
