#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for AppDynamics REST API
"""

from test import ApplicationApiTest

class V1_ApplicationTest(ApplicationApiTest):

    def test_app_list(self):
        apps = self.c.get_applications()
        self.assertEqual(len(apps), 1)
        self.assertEqual(apps[0].id, 10)
        self.assertEqual(apps[0].name, 'ACME Book Store Application')

    def test_get_app_by_name(self):
        apps = self.c.get_applications()
        self.assertEqual(apps.by_name('ACME Book Store Application').id, 10)

    def test_get_config_by_name(self):
        config = self.c.get_config()
        val = config.by_name('metrics.retention.period')
        self.assertEqual(val.name, 'metrics.retention.period')
        self.assertEqual(val.value, '365')
