#! /usr/bin/env python

# __author__ = 'Todd Radel <tradel@appdynamics.com>'

from setuptools import setup

setup(name='AppDynamicsREST',
      version='0.2.0',
      description='Python SDK for AppDynamics REST API',
      author='Todd Radel',
      author_email='tradel@appdynamics.com',
      url='https://github.com/tradel/AppDynamicsREST',
      download_url='https://github.com/tradel/AppDynamicsREST',
      packages=['appd'],
      package_data={'': ['README.md', 'data/*', 'examples/*']},
      install_requires=['requests'],
      extras_require={'examples': ['lxml', 'tzlocal']}
      )
