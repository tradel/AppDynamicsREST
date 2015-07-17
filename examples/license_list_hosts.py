#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import itertools
import csv

from appd.cmdline import parse_argv
from appd.request import AppDynamicsClient


__author__ = 'Todd Radel'
__copyright__ = 'Copyright (c) 2013-2015 AppDynamics Inc.'
__version__ = '0.4.5'


def incr(d, name, amt=1):
    d[name] = d.get(name, 0) + amt


args = parse_argv()
c = AppDynamicsClient(args.url, args.username, args.password, args.account, args.verbose)

nodes = []
for app in c.get_applications():
    for node in c.get_nodes(app.id):

        node.app_id = app.id
        node.app_name = app.name

        if node.has_machine_agent or node.has_app_agent:
            if node.has_app_agent:
                if 'PHP' in node.type:
                    node.group_type = 'PHP App Agent'
                if 'IIS' in node.type:
                    node.group_type = '.NET App Agent'
                else:
                    node.group_type = 'Java App Agent'
            else:
                node.group_type = 'Machine Agent only'

            nodes.append(node)


# Sort and group the nodes by machine_id.

group_func = lambda x: x.machine_id
nodes.sort(key=group_func)

with open('data/licenses_by_host.csv', 'w') as f:
    w = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, dialect=csv.excel)

    hdr = ['App Name', 'Host Name', 'Host Type', 'License Count']
    w.writerow(hdr)

    for machine_id, nodes_on_machine_iter in itertools.groupby(nodes, key=group_func):

        nodes_on_machine = list(nodes_on_machine_iter)
        first_node = nodes_on_machine[0]
        agent_type = first_node.group_type
        types = [x.group_type for x in nodes_on_machine]
        all_same = all(x.group_type == agent_type for x in nodes_on_machine)
        assert all_same, first_node

        license_count = 1
        if 'Java' in agent_type:
            license_count = len(nodes_on_machine)

        w.writerow([first_node.app_name, first_node.machine_name, agent_type, license_count])
        
        

