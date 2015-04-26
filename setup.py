#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# __author__ = 'Todd Radel <tradel@appdynamics.com>'

from setuptools import setup
import io
import os
import sys

import appd

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

setup(name='AppDynamicsREST',
      version=appd.__version__,
      description='AppDynamics REST API Library',
      long_description=read('README.rst'),
      author='Todd Radel',
      author_email='tradel@appdynamics.com',
      url='https://github.com/tradel/AppDynamicsREST',
      packages=['appd'],
      platforms='any',
      package_data={'': ['README.md', 'data/*', 'examples/*', 'templates/*']},
      install_requires=['requests', 'argparse', 'six'],
      extras_require={'examples': ['lxml', 'tzlocal', 'jinja2'], 'testing': ['nose']},
      test_suite='nose.collector',
      tests_require=['nose'],
      license='Apache',
      classifiers=[
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'Development Status :: 4 - Beta',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: System :: Monitoring',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4'],
)
