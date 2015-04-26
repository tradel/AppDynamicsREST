
============================
AppDynamics REST API Library
============================

Current version: 0.4.1-dev

Released: 23-Apr-2015

.. image:: https://travis-ci.org/tradel/AppDynamicsREST.svg?branch=master
   :target: https://travis-ci.org/tradel/AppDynamicsREST/

.. image:: https://pypip.in/d/AppDynamicsREST/badge.svg
   :target: https://pypi.python.org/pypi/AppDynamicsREST/


Introduction
------------

AppDynamicsREST is a library that provides a clean Python interface to the
REST API of an AppDynamics controller.

AppDynamicsREST is developed using Python 2.7.6 on Mac OSX. It is known to
work on most Linux distributions and on Windows with Python 2.6, 2.7,
3.3, or 3.4.


Installation
------------

Install via ``pip``::

    $ pip install AppDynamicsREST

Install from source::

    $ git clone git://github.com/tradel/AppDynamicsREST.git
    $ cd AppDynamicsREST
    $ python setup.py install


Prerequisites
-------------

 * `requests <https://pypi.python.org/pypi/requests>`_
 * `argparse <https://pypi.python.org/pypi/argparse>`_
 * `nose <https://pypi.python.org/pypi/nose>`_ (for running unit tests)
 * `tzlocal <https://pypi.python.org/pypi/tzlocal>`_ and
   `lxml <https://pypi.python.org/pypi/lxml>`_
   (used by some of the example scripts)
 * `jinja2 <https://pypi.python,org/pypi/jinja2>`_ (used by the audit report example)


Documentation
-------------

The documentation is hosted online at readthedocs.org_.


A Quick Example
---------------

Here's a simple example that retrieves a list of business applications
from a controller on localhost, and prints them out:

.. code:: python

    from appd.request import AppDynamicsClient

    c = AppDynamicsClient('http://localhost:8090', 'user1', 'password', 'customer1', verbose=True)
    for app in c.get_applications():
        print app.name, app.id


Testing
-------

If you have cloned the repo, you can run the unit tests from ``setup.py``::

    python setup.py test

Or, if you have ``nose`` installed, you can use that::

    nosetests


For More Information
--------------------

The main source repo is on Github_.

To ask a question or join the discussion, visit the AppDynamics `Community page`_.



.. _AppDynamics: http://www.appdynamics.com/
.. _Github: https://github.com/tradel/AppDynamicsREST
.. _Community page: http://community.appdynamics.com/t5/eXchange-Community-AppDynamics/Python-SDK-for-Controller-REST-API/idi-p/917
.. _readthedocs.org: http://appdynamicsrest.readthedocs.org/en/latest/