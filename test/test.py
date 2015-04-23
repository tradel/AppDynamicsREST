"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""

__author__ = 'Todd Radel <tradel@appdynamics.com>'

import unittest
from appd.model import *
from appd.request import AppDynamicsClient


class ApplicationApiTest(unittest.TestCase):

    test_url = 'http://ec2-54-237-61-120.compute-1.amazonaws.com:8090'
    test_user = 'user1'
    test_pass = 'welcome'
    test_acct = 'customer1'

    def setUp(self):
        self.c = AppDynamicsClient(self.test_url, self.test_user, self.test_pass, self.test_acct)

    def test_app_list(self):
        apps = self.c.get_applications()
        self.assertEqual(len(apps), 2)
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


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ApplicationApiTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
