#! /usr/bin/env python2.7

"""
Helper script to regenerate reStructuredText from Markdown. Uses pandoc.
"""

import pandoc
import os

pandoc.core.PANDOC_PATH = '/usr/local/bin/pandoc'

doc = pandoc.Document()
doc.markdown = open('README.md').read()
f = open('docs/appsphere.rst','w+')
f.write(doc.rst)
f.close()
os.system("./setup.py register")

