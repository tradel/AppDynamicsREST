__author__ = 'tradel'

import argparse


def parse_argv():
    parser = argparse.ArgumentParser(description='Gets a count of licenses in use from an AppDynamics controller.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-c', '--url', dest='url', help='set the controller URL')
    parser.add_argument('-u', '--username', dest='username', help='set the username for authentication')
    parser.add_argument('-p', '--password', dest='password', help='set the password for authentication')
    parser.add_argument('-a', '--account', default='customer1', dest='account',
                        help='set the controller account (default: customer1)')
    return parser.parse_args()

