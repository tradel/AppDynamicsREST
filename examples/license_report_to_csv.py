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


args = parse_argv()
c = AppDynamicsClient(args.url, args.username, args.password, args.account, args.verbose)

nodes = []
for app in c.get_applications():
    for node in c.get_nodes(app.id):
        node_type = node.type
        if node.has_machine_agent and not node.has_app_agent:
            node.type = 'Machine Agent'
        nodes.append(node)


# Sort and group the nodes by machine_id.

group_func = lambda x: (x.machine_id, x.type)
nodes.sort(key=group_func)

tier_names = set()
tiers = dict()
for machine_id, nodes_on_machine_iter in itertools.groupby(nodes, key=group_func):

    nodes_on_machine = list(nodes_on_machine_iter)
    agent_type = nodes_on_machine[0].type
    tier_name = nodes_on_machine[0].tier_name.split('.')[0]

    license_count = len(nodes_on_machine)
    if 'PHP' in agent_type:
        agent_type = 'PHP'
    if 'IIS' in agent_type:
        agent_type = 'DOT_NET'
        license_count = 1
    elif agent_type == 'Machine Agent':
        agent_type = 'MACHINE'
        license_count = 1
        assert len(nodes_on_machine) == 1
    else:
        agent_type = 'JAVA'

    def key(name):
        return '%s|%s|%s' % (tier_name, agent_type, name)

    def incr(name, amt=1):
        k = key(name)
        tiers[k] = tiers.get(k, 0) + amt

    incr('licenses', license_count)
    incr('agents', len(nodes_on_machine))
    tiers.setdefault(key('host_set'), set()).add(machine_id[0])
    tiers[key('hosts')] = len(tiers[key('host_set')])
    tier_names.add(tier_name)


AGENT_TYPES = ('JAVA', 'DOT_NET', 'PHP', 'MACHINE')

with open('data/licenses.csv', 'w') as f:
    w = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, dialect=csv.excel)

    hdr = ['Tier Name', 'Java Licenses', 'Java Agents', 'Java Hosts', '.NET Licenses', '.NET Agents', '.NET Hosts',
           'PHP Licenses', 'PHP Agents', 'PHP Hosts', 'Machine Agent Licenses', 'Machine Agents', 'Machine Agent Hosts']
    w.writerow(hdr)

    for tier_name in sorted(tier_names):
        row = [tier_name]
        for agent_type in AGENT_TYPES:
            def get(name):
                return tiers.get('%s|%s|%s' % (tier_name, agent_type, name), 0)
            row.extend([get('licenses'), get('agents'), get('hosts')])
        w.writerow(row)
