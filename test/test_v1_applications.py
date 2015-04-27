#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for AppDynamics REST API
"""

from test import ApplicationApiTest

class V1_ApplicationTest(ApplicationApiTest):

    def test_app_list(self):
        apps = self.c.get_applications()
        self.assertEqual(len(apps), 3)
        self.assertEqual(apps[0].id, 4)
        self.assertEqual(apps[0].name, 'ECommerce')
        self.assertEqual(apps[1].id, 6)
        self.assertEqual(apps[1].name, 'Fulfillment')

    def test_get_app_by_name(self):
        apps = self.c.get_applications()
        self.assertEqual(apps.by_name('ECommerce').id, 4)
        self.assertEqual(apps.by_name('Fulfillment').id, 6)

    def test_get_config_by_name(self):
        config = self.c.get_config()
        val = config.by_name('metrics.retention.period')
        self.assertEqual(val.name, 'metrics.retention.period')
        self.assertEqual(val.value, '365')
