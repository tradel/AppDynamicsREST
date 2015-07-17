#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sample script to print a list of all external dependencies for an application.
This would include databases, message queues, web sites,
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

app_name = 'E-Commerce_Demo'
tier_name = 'ECommerce-Server'
metric_path = 'Overall Application Performance|' + tier_name + '|External Calls'

app_id = -1
for app in c.get_applications():
    if app.name == app_name:
        app_id = app.id

deps = c.get_metric_tree(app_id, metric_path)
for dep in deps:
    if dep.type == 'folder':
        print(dep.name)

