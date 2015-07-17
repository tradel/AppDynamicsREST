#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script generates a report of response times, calls, and errors for all the backends registered
on a controller. The output is generated as XML and can be sent to a file with this syntax::

    python BackendMetrics.py > metric_output.xml

By default this will connect to a controller on localhost:8090. The script accepts command-line
arguments to change the connection parameters:

--controller=<url>
--account=<account>
--username=<name>
--password=<password>

Example::
    python BackendMetrics.py --controller=http://10.1.2.3:8090 --account=customer1 --username=demo --password=abc123
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

time_in_mins = 24 * 60
end_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
end_epoch = int(mktime(end_time.timetuple())) * 1000


# Metric mapper
#
# Uses a hash table to call the function appropriate for specific metric types, e.g.: calls map_art for
# Average Response Time, map_cpm for Calls per Minute, etc.

def map_art(d, metric_total, metric_average, metric_sum, max_point):
    d['art'] = metric_average


def map_cpm(d, metric_total, metric_average, metric_sum, max_point):
    d['total_calls'] = metric_total
    d['cpm_average'] = metric_average
    d['cpm_max'] = max_point[0]
    d['cpm_max_time'] = max_point[1]


def map_err(d, metric_total, metric_average, metric_sum, max_point):
    d['total_errors'] = metric_total
    d['epm_avg'] = metric_average
    d['epm_max'] = max_point[0]
    d['epm_max_time'] = max_point[1]


def no_such_metric(d, metric_total, metric_average, metric_sum, max_point):
    raise ValueError("no such metric")


METRIC_DISPATCHER = {
    'Average Response Time (ms)': map_art,
    'Calls per Minute': map_cpm,
    'Errors per Minute': map_err,
    'DEFAULT': no_such_metric
}


# Helper functions

def now_rfc3339():
    return datetime.now(tzlocal.get_localzone()).isoformat('T')


def freq_to_mins(md):
    FREQ_MAP = {'ONE_MIN': 1, 'TEN_MIN': 10, 'SIXTY_MIN': 60}
    return FREQ_MAP[md.frequency]


# Parse command line arguments and create AD client:

args = parse_argv()
c = AppDynamicsClient(args.url, args.username, args.password, args.account, args.verbose)


# Get the list of configured apps, and get backend metrics for each one:

rows = defaultdict(dict)
for app in c.get_applications():
    for md in c.get_metrics('Backends|*|*', app.id, time_range_type='BEFORE_TIME', end_time=end_epoch,
                            duration_in_mins=time_in_mins, rollup=False):

        # Get the last two components of the metric path. This should be 'backend_name|metric_name'.
        backend_name, metric_name = md.path.split('|')[-2:]

        if 'Discovered backend call' in backend_name:
            backend_name = backend_name[26:]
            metric_sum = sum([x.value for x in md.values])
            metric_total = metric_sum * freq_to_mins(md)
            metric_average = 0
            max_point = (0, None)
            if len(md.values) > 0:
                metric_average = metric_sum / len(md.values)
                max_point = max([(max(x.value, x.current, x.max), x.start_time) for x in md.values])

            func = METRIC_DISPATCHER.get(metric_name, None)
            if func:
                func(rows[backend_name], metric_total, metric_average, metric_sum, max_point)
                rows[backend_name]['app'] = app.name

# Generate the report.

XSI = 'http://www.w3.org/2001/XMLSchema-instance'
E = ElementMaker(nsmap={'xsi': XSI})

root = E.BackendResponseTimes(Controller=c.base_url, GenerationTime=now_rfc3339())
root.set('{%s}noNamespaceSchemaLocation' % XSI, 'backend_metrics.xsd')

for k, v in sorted(rows.items()):
    v.setdefault('cpm_max_time', '')
    v.setdefault('epm_max_time', '')
    root.append(E.Backend(
        E.ApplicationName(v['app']),
        E.BackendName(k),
        E.AverageResponseTime(str(v.get('art', 0))),
        E.CallsPerMinute(str(v.get('cpm_average', 0))),
        E.TotalCalls(str(v.get('total_calls', 0))),
        E.MaximumCallsPerMinute(str(v.get('cpm_max', 0))),
        E.MaximumCallTime(v['cpm_max_time'].isoformat('T') if v['cpm_max_time'] else ''),
        E.ErrorsPerMinute(str(v.get('epm_avg', 0))),
        E.TotalErrors(str(v.get('total_errors', 0))),
        E.MaximumErrorsPerMinute(str(v.get('epm_max', 0))),
        E.MaximumErrorTime(v['epm_max_time'].isoformat('T') if v['epm_max_time'] else ''),
    ))

# Print the report to stdout.

print(etree.ProcessingInstruction('xml', 'version="1.0" encoding="UTF-8"'))
print(etree.tostring(root, pretty_print=True, encoding='UTF-8'))
