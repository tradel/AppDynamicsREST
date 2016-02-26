#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for AppDynamics REST API
"""

import unittest
import logging
from unittest.util import safe_repr

import appd
import creds.demo2 as creds

__author__ = 'Todd Radel'
__copyright__ = 'Copyright (c) 2013-2015 AppDynamics Inc.'
__version__ = '0.4.5'


class ApplicationApiTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.WARN)
        self.c = appd.request.AppDynamicsClient(creds.url, creds.user, creds.password, creds.account)

    def assertIn(self, member, container, msg=None):
        """Just like self.assertTrue(a in b), but with a nicer default message."""
        if member not in container:
            standard_msg = '%s not found in %s' % (safe_repr(member),
                                                   safe_repr(container))
            self.fail(self._formatMessage(msg, standard_msg))

    def assertNotIn(self, member, container, msg=None):
        """Just like self.assertTrue(a not in b), but with a nicer default message."""
        if member in container:
            standard_msg = '%s unexpectedly found in %s' % (safe_repr(member),
                                                            safe_repr(container))
            self.fail(self._formatMessage(msg, standard_msg))


if __name__ == '__main__':
    from test_v1_applications import *
    from test_v1_metric_tree import *
    from test_v2_accounts import *
    from test_v2_license_modules import *

    suite = unittest.TestLoader() \
        .loadTestsFromTestCase(V1_ApplicationTest) \
        .loadTestsFromTestCase(V1_MetricTreeTest) \
        .loadTestsFromTestCase(V2_AccountTest) \
        .loadTestsFromTestCase(V2_LicenseModuleTest)

    unittest.TextTestRunner(verbosity=2).run(suite)
