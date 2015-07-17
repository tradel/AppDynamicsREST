#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sample script to generate a list of all health rule violations that occurred yesterday.
"""

from __future__ import print_function

from datetime import datetime

from appd.cmdline import parse_argv
from appd.request import AppDynamicsClient
from appd.time import from_ts, to_ts


__author__ = 'Todd Radel'
__copyright__ = 'Copyright (c) 2013-2015 AppDynamics Inc.'
__version__ = '0.4.5'


# Parse the command line arguments and initialize the client
#
args = parse_argv()
c = AppDynamicsClient(args.url, args.username, args.password, args.account, args.verbose)

# Get the application list and find "MyApp"
#
apps = c.get_applications()
gn_prod = [x for x in apps if x.name == "MyApp"][0]

# Calculate start and end times for the report: 24h period ending with midnight last night
#
today = to_ts(datetime.now().date())
yesterday = today - (86400 * 1000)

# Get the list of nodes so we can look up by node_id
#
all_nodes = c.get_nodes(gn_prod.id)
nodes_by_id = dict(list(zip([x.id for x in all_nodes], all_nodes)))

# Get all health rule violations and print them
#
violations = c.get_healthrule_violations(gn_prod.id, 'BETWEEN_TIMES', start_time=yesterday, end_time=today)
for v in violations:
    print("-" * 70)
    print("Start time:   ", from_ts(v.start_time_ms))
    print("End time:     ", from_ts(v.end_time_ms))
    print("Description:  ", v.description)
    print("Details:      ", v.deep_link_url)
    if v.affected_entity.type == "APPLICATION_COMPONENT_NODE":
        try:
            print("Affected Node: ", nodes_by_id[v.affected_entity.entity_id].name)
        except KeyError:
            print("Affected Node: UNKNOWN")

