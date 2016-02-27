#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for AppDynamics REST API
"""

import tzlocal
from datetime import datetime, timedelta

from test import ApplicationApiTest


def now():
    my_tz = tzlocal.get_localzone()
    return datetime.now(my_tz).replace(microsecond=0)


def midnight():
    return now().replace(hour=0, minute=0, second=0, microsecond=0)


class V2_LicenseUsageTest(ApplicationApiTest):
    def test_license_usage_java(self):
        usage = self.c.get_license_usage(2, 'java', midnight() - timedelta(hours=24), midnight() - timedelta(hours=1))
        for x in usage.usages:
            self.assertEqual(x.license_module, 'java')
            self.assertEqual(x.account_id, 2)
            self.assertEqual(x.sample_count, 12)
            self.assertEqual(x.avg_units_provisioned, 100)
            self.assertEqual(x.avg_units_allowed, 100)
        self.assertEqual(len(usage.usages), 24, 'License usage should return 24 data points')

    def test_license_usage_java_5min(self):
        usage = self.c.get_license_usage_5min(2, 'java', now() - timedelta(hours=1), now())
        for x in usage.usages:
            self.assertEqual(x.license_module, 'java')
            self.assertEqual(x.account_id, 2)
            self.assertEqual(x.units_allowed, 100)
            self.assertEqual(x.units_provisioned, 100)
        self.assertEqual(len(usage.usages), 12, 'License usage should return 12 data points')
