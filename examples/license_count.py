#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from datetime import datetime
import itertools

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
        # node_type = node.type
        # print node.id, node.machine_id, node.machine_name, node.type
        # print node.type, node.os_type, node.app_agent_version
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

host_counts = dict()
node_counts = dict()
lic_counts = dict()
for machine_id, nodes_on_machine_iter in itertools.groupby(nodes, key=group_func):

    nodes_on_machine = list(nodes_on_machine_iter)
    first_node = nodes_on_machine[0]
    agent_type = first_node.group_type
    # types = [x.group_type for x in nodes_on_machine]
    # all_same = all(x.group_type == agent_type for x in nodes_on_machine)
    # print all_same, types
    # assert all_same, first_node

    license_count = 1
    if 'Java' in agent_type:
        license_count = len(nodes_on_machine)

    incr(lic_counts, agent_type, license_count)
    incr(host_counts, agent_type, 1)
    incr(node_counts, agent_type, len(nodes_on_machine))

    # if '.NET' in agent_type:
    #     node_names = [x.name for x in nodes_on_machine]
    #     print 'Host:', first_node.machine_name, '\n\t', '\n\t'.join(node_names)


# Print the results.
tot_nodes, tot_hosts, tot_licenses = (0, 0, 0)
header_fmt = '%-30s %-15s %-15s %s'
data_fmt = '%-30s %15d %15d %15d'

print()
print('License usage report for ' + args.url)
print('Generated at: ' + str(datetime.now()))
print()
print(header_fmt % ('Node Type', 'Node Count', 'Host Count', 'License Count'))
print(header_fmt % ('=' * 30, '=' * 15, '=' * 15, '=' * 15))

for node_type in ('Java App Agent', '.NET App Agent', 'PHP App Agent', 'Machine Agent only'):
    node_count = node_counts.get(node_type, 0)
    host_count = host_counts.get(node_type, 0)
    lic_count = lic_counts.get(node_type, 0)
    tot_nodes += node_count
    tot_hosts += host_count
    tot_licenses += lic_count
    print(data_fmt % (node_type, node_count, host_count, lic_count))

print(header_fmt % ('=' * 30, '=' * 15, '=' * 15, '=' * 15))
print(data_fmt % ('TOTAL', tot_nodes, tot_hosts, tot_licenses))
