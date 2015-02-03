#! /usr/bin/env python2.7

# __author__ = 'Todd Radel <tradel@appdynamics.com>'

from setuptools import setup
import os

long_description = 'Python SDK for AppDynamics REST API'
if os.path.exists('docs/appsphere.rst'):
    long_description = open('docs/appsphere.rst').read()

setup(name='AppDynamicsREST',
      version='0.3.0',
      description='Python SDK for AppDynamics REST API',
      author='Todd Radel',
      author_email='tradel@appdynamics.com',
      url='https://github.com/tradel/AppDynamicsREST',
      download_url='https://github.com/tradel/AppDynamicsREST',
      packages=['appd'],
      package_data={'': ['README.md', 'data/*', 'examples/*', 'templates/*']},
      install_requires=['requests'],
      extras_require={'examples': ['lxml', 'tzlocal']}
      )
