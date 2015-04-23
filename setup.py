#! /usr/bin/env python2.7

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

long_description = read('README.rst')

setup(name='AppDynamicsREST',
      version=appd.__version__,
      description='Python SDK for AppDynamics REST API',
      author='Todd Radel',
      author_email='tradel@appdynamics.com',
      url='https://github.com/tradel/AppDynamicsREST',
      download_url='https://github.com/tradel/AppDynamicsREST',
      packages=['appd'],
      platforms='any',
      package_data={'': ['README.md', 'data/*', 'examples/*', 'templates/*']},
      install_requires=['requests', 'argparse', 'future'],
      extras_require={'examples': ['lxml', 'tzlocal'], 'testing': ['nose']},
      tests_require=['nose'],
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 4 - Beta',
          'Natural Language :: English',
          'Topic :: System :: Monitoring',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],

)
