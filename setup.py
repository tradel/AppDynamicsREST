#! /usr/bin/env python

# __author__ = 'Todd Radel <tradel@appdynamics.com>'

from setuptools import setup

setup(name='AppDynamicsREST',
      version='0.1.2',
      description='REST API client for AppDynamics Controllers',
      author='Todd Radel',
      author_email='tradel@appdynamics.com',
      url='https://github.com/tradel/AppDynamicsREST',
      download_url='https://github.com/tradel/AppDynamicsREST',
      packages=['appd'],
      package_data={'appd': ['README.md', 'data/*', 'examples/*']},
      install_requires=['requests', 'lxml', 'tzlocal']
      )
