#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for AppDynamics REST API
"""

import unittest
from test import ApplicationApiTest


class V2_LicenseModuleTest(ApplicationApiTest):

    def test_license_modules(self):
        mods = self.c.get_license_modules(2)
        self.assertIn('java', mods.modules)
        self.assertIn('dot-net', mods.modules)
        self.assertNotIn('wharrgarbl', mods.modules)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(V2_LicenseModuleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
