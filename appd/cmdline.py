"""
Command line parsing for REST API scripts.
"""

import argparse


def parse_argv(app_desc=None):
    """
    Provides a parser for a standard set of command line options.

    Use of this function is optional but highly encouraged, as it allows all scripts based on the SDK to be
    invoked in a familiar way.

    :param str app_desc: Short description of your application, to be printed when help is requested.
    :returns: a Namespace full of parsed arguments
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(description=app_desc)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Enable verbose output')
    parser.add_argument('-c', '--url', dest='url', required=True,
                        help='set the controller URL')
    parser.add_argument('-u', '--username', dest='username', required=True,
                        help='set the username for authentication')
    parser.add_argument('-p', '--password', dest='password', required=True,
                        help='set the password for authentication')
    parser.add_argument('-a', '--account', default='customer1', dest='account',
                        help='set the controller account (default: customer1)')
    return parser.parse_args()

