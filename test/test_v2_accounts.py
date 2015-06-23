#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for AppDynamics REST API
"""

from test import ApplicationApiTest


class V2_AccountTest(ApplicationApiTest):

    def test_my_account(self):
        acct = self.c.get_my_account()
        self.assertEqual(acct.id, '2')
        self.assertEqual(acct.name, 'customer1')

    def test_get_account_by_id(self):
        acct = self.c.get_account(2)
        self.assertEqual(acct.id, '2')
        self.assertEqual(acct.name, 'customer1')
