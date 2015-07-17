#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script generates a report of response times, calls, and errors for all the BT's registered
on a controller. The output is generated as XML and can be sent to a file with this syntax::

    python BusinessTransactionsMetrics.py > metric_output.xml

By default this will connect to a controller on localhost:8090. The script accepts command-line
arguments to change the connection parameters:

--controller=<url>
--account=<account>
--username=<name>
--password=<password>

Example::
     python BTMetrics.py --controller=http://10.1.2.3:8090 --account=customer1 --username=demo --password=abc123
"""

from __future__ import print_function

from collections import defaultdict
from datetime import datetime
from time import mktime
from lxml.builder import ElementMaker
from lxml import etree
import tzlocal

from appd.cmdline import parse_argv
from appd.request import AppDynamicsClient


__author__ = 'Todd Radel'
__copyright__ = 'Copyright (c) 2013-2015 AppDynamics Inc.'
__version__ = '0.4.5'


# The report will generate data for the 24-hour period before midnight of the current day. To change the
# reporting period, adjust these variables.

time_in_mins = 1440
end_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
end_epoch = int(mktime(end_time.timetuple())) * 1000


# Helper functions

def now_rfc3339():
    return datetime.now(tzlocal.get_localzone()).isoformat('T')


# Parse command line arguments and create AD client:

args = parse_argv()
c = AppDynamicsClient(args.url, args.username, args.password, args.account, args.verbose)


# Get the list of configured apps, and get backend metrics for each one:

METRIC_MAP = {'Average Block Time (ms)': 'abt',
              'Average CPU Used (ms)': 'cpu',
              'Average Request Size': 'req_size',
              'Average Response Time (ms)': 'art',
              'Average Wait Time (ms)': 'wait_time',
              'Calls per Minute': 'cpm',
              'End User Average Response Time (ms)': 'eum_art',
              'End User Network Average Response Time (ms)': 'eum_net',
              'End User Page Render Average Response Time (ms)': 'eum_render',
              'Errors per Minute': 'epm',
              'Normal Average Response Time (ms)': 'norm_art',
              'Number of Slow Calls': 'slow',
              'Number of Very Slow Calls': 'veryslow',
              'Stall Count': 'stalls'}


empty_row = dict([(x, 0) for x in list(METRIC_MAP.values())])
rows = defaultdict(dict)

for app in c.get_applications():

    bt_list = c.get_bt_list(app.id)

    for md in c.get_metrics('Business Transaction Performance|Business Transactions|*|*|*',
                            app.id, time_range_type='BEFORE_TIME', end_time=end_epoch,
                            duration_in_mins=time_in_mins, rollup=True):

        # Get the last 3 components of the metric path. This should be 'tier_name|bt_name|metric_name'.
        tier_name, bt_name, metric_name = md.path.split('|')[-3:]
        tier_bts = bt_list.by_tier_and_name(bt_name, tier_name)
        if tier_bts:
            bt = tier_bts[0]
            if len(md.values) > 0 and metric_name in METRIC_MAP:
                key = (tier_name, bt_name)
                rows.setdefault(key, empty_row.copy()).update({'app_id': app.id,
                                                               'app_name': app.name,
                                                               'bt_id': bt.id,
                                                               'bt_name': bt.name,
                                                               'tier_name': bt.tier_name,
                                                               'type': bt.type,
                                                               METRIC_MAP[metric_name]: md.values[0].value})


# Generate the report.

XSI = 'http://www.w3.org/2001/XMLSchema-instance'
E = ElementMaker(nsmap={'xsi': XSI})

root = E.BusinessTransactions(Controller=c.base_url, GenerationTime=now_rfc3339())
root.set('{%s}noNamespaceSchemaLocation' % XSI, 'bt_metrics.xsd')

for k, v in sorted(rows.items()):
    v['calls'] = v['cpm'] * time_in_mins
    v['errors'] = v['epm'] * time_in_mins
    v['error_pct'] = round(float(v['errors']) / float(v['calls']) * 100.0, 1) if v['calls'] > 0 else 0

    root.append(E.BusinessTransaction(
        E.ApplicationName(v['app_name']),
        E.BusinessTransactionName(v['bt_name']),
        E.TierName(v['tier_name']),
        E.AverageResponseTime(str(v['art'])),
        E.CallsPerMinute(str(v['cpm'])),
        E.TotalCalls(str(v['calls'])),
        E.TotalErrors(str(v['errors'])),
        E.ErrorsPerMinute(str(v['epm'])),
        E.ErrorPercentage(str(v['error_pct'])),
        E.SlowCalls(str(v['slow'])),
        E.VerySlowCalls(str(v['veryslow'])),
        E.Stalls(str(v['stalls'])),
    ))


# Print the report to stdout.

print(etree.ProcessingInstruction('xml', 'version="1.0" encoding="UTF-8"'))
print(etree.tostring(root, pretty_print=True, encoding='UTF-8'))
