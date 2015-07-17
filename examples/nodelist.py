#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sample script to print a simple list of all the nodes registered with the controller.
Output format: ``app_name,tier_name,node_name,host_name``
"""

from __future__ import print_function

from appd.cmdline import parse_argv
from appd.request import AppDynamicsClient

__author__ = 'Todd Radel'
__copyright__ = 'Copyright (c) 2013-2015 AppDynamics Inc.'
__version__ = '0.4.5'


args = parse_argv()
c = AppDynamicsClient(args.url, args.username, args.password, args.account, args.verbose)

for app in c.get_applications():
    for node in c.get_nodes(app.id):
        print(','.join([app.name, node.tier_name, node.name, node.machine_name]))

