#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for AppDynamics REST API
"""

from test import ApplicationApiTest

class V1_MetricTreeTest(ApplicationApiTest):

    def test_root_categories(self):
        nodes = self.c.get_metric_tree(12)
        self.assertEqual(nodes.by_name('Errors').type, 'folder')
        self.assertEqual(nodes.by_name('Backends').type, 'folder')
        self.assertEqual(nodes.by_name('Overall Application Performance').type, 'folder')
        self.assertEqual(nodes.by_name('Business Transaction Performance').type, 'folder')
        self.assertEqual(nodes.by_name('Application Infrastructure Performance').type, 'folder')
        self.assertEqual(nodes.by_name('Information Points').type, 'folder')

    def test_not_found(self):
        nodes = self.c.get_metric_tree(12)
        self.assertRaises(KeyError, nodes.by_name, 'Foobar')

    def test_level_2_bt(self):
        nodes = self.c.get_metric_tree(12, 'Business Transaction Performance')
        self.assertEqual(nodes.by_name('Business Transactions').type, 'folder')
        self.assertEqual(nodes.by_name('Business Transaction Groups').type, 'folder')
        self.assertRaises(KeyError, nodes.by_name, 'Business Transaction Performance')

    def test_level_2_aip(self):
        nodes = self.c.get_metric_tree(12, 'Application Infrastructure Performance')
        self.assertEqual(nodes.by_name('CoreServices').type, 'folder')
        self.assertEqual(nodes.by_name('ConfirmationSyncService').type, 'folder')

    def test_recurse_(self):
        nodes = self.c.get_metric_tree(12, 'Application Infrastructure Performance|CoreServices|Agent', recurse=True)
        self.assertEqual(nodes.by_name('App').type, 'folder')
        app_nodes = nodes.by_name('App').children
        self.assertEqual(app_nodes.by_name('Availability').type, 'leaf')

        self.assertEqual(nodes.by_name('Machine').type, 'folder')
        machine_nodes = nodes.by_name('App').children
        self.assertEqual(machine_nodes.by_name('Availability').type, 'leaf')
