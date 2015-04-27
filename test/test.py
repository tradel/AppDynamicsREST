#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for AppDynamics REST API
"""

import unittest
import appd
import creds.ec2 as creds

__author__ = 'Todd Radel'
__copyright__ = 'Copyright (c) 2013-2015 AppDynamics Inc.'
__version__ = '0.4.1'


class ApplicationApiTest(unittest.TestCase):

    def setUp(self):
        self.c = appd.request.AppDynamicsClient(creds.url, creds.user, creds.password, creds.account)


if __name__ == '__main__':
    from test_v1_applications import *
    from test_v2_accounts import *
    from test_v2_license_modules import *
    suite = unittest.TestLoader()\
        .loadTestsFromTestCase(V1_ApplicationTest)\
        .loadTestsFromTestCase(V2_AccountTest)\
        .loadTestsFromTestCase(V2_LicenseModuleTest)

    unittest.TextTestRunner(verbosity=2).run(suite)
