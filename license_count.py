#! python

__author__ = 'tradel'

from appd.cmdline import parse_argv
from appd.request import AppDynamicsClient
from collections import defaultdict
from datetime import datetime
import itertools
import tzlocal

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
licenses, agents, hosts = defaultdict(int), defaultdict(int), defaultdict(set)

for machine_id, nodes_on_machine_iter in itertools.groupby(nodes, key=group_func):

    nodes_on_machine = list(nodes_on_machine_iter)
    agent_type = nodes_on_machine[0].type

    if 'PHP' in agent_type:
        agent_type = 'PHP app server'
        licenses[agent_type] += len(nodes_on_machine)
    if 'IIS' in agent_type:
        agent_type = '.NET app server'
        licenses[agent_type] += 1
    elif agent_type == 'Machine Agent':
        agent_type = 'Machine Agent only'
        assert len(nodes_on_machine) == 1
        licenses[agent_type] += 1
    else:
        agent_type = 'Java app server'
        licenses[agent_type] += len(nodes_on_machine)

    agents[agent_type] += len(nodes_on_machine)
    hosts[agent_type].add(machine_id[0])


# Print the report.

fmt = '%-25s %10d %10d %10d'
h_fmt = fmt.replace('%10d', '%-10s')

print
print 'License report for: ', c.base_url
print 'Run on:             ', datetime.now(tzlocal.get_localzone()).strftime('%a, %d %b %Y %H:%M:%S %Z %z')
print
print h_fmt % ('Node Type', 'Licenses', 'Nodes', 'Hosts')
print h_fmt % ('=' * 25, '=' * 10, '=' * 10, '=' * 10)

for agent_type in sorted(licenses.keys()):
    print fmt % (agent_type, licenses[agent_type], agents[agent_type], len(hosts[agent_type]))

total_licenses = sum([v for v in licenses.values()])
total_agents = sum([v for v in agents.values()])
total_hosts = sum([len(v) for v in hosts.values()])

print h_fmt % ('=' * 25, '=' * 10, '=' * 10, '=' * 10)
print fmt % ('TOTALS', total_licenses, total_agents, total_hosts)
print
