#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for AppDynamics REST API
"""

from test import ApplicationApiTest


class V1_ApplicationTest(ApplicationApiTest):

    def test_app_list(self):
        apps = self.c.get_applications()
        self.assertEqual(len(apps), 4)
        self.assertEqual(apps[0].id, 12)
        self.assertEqual(apps[0].name, 'Movie Tickets Online')

    def test_get_app_by_name(self):
        apps = self.c.get_applications()
        self.assertEqual(apps.by_name('Movie Tickets Online').id, 12)

    def test_get_config_by_name(self):
        config = self.c.get_config()
        val = config.by_name('metrics.retention.period')
        self.assertEqual(val.name, 'metrics.retention.period')
        self.assertEqual(val.value, '365')
