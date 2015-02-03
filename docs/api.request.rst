
:mod:`appd.request` - AppDynamics REST Access
=============================================

.. module:: appd.request

.. toctree::
   :maxdepth: 4

AppDynamicsClient class
-----------------------

.. autoclass:: AppDynamicsClient
   :members:

Notes
-----

.. _time-range-types:

Specifying Time Ranges
^^^^^^^^^^^^^^^^^^^^^^

When you are asking for metrics or snapshots, you must specify a time range for the controller to search within.
Depending on the type of time range you select, you must provide additional parameters to the query. Here are the
time range types and their required parameters:

+-----------------+----------------------------------+--------------------------------------+
| Time Range Type | Required Fields                  | Meaning                              |
+=================+==================================+======================================+
| BEFORE_NOW      | `duration_in_mins`               | Same as "last `x` minutes".          |
+-----------------+----------------------------------+--------------------------------------+
| BEFORE_TIME     | `end_time`, `duration_in_mins`   | `x` minutes before `end_time`.       |
+-----------------+----------------------------------+--------------------------------------+
| AFTER_TIME      | `start_time`, `duration_in_mins` | `x` minutes after `start_time`.      |
+-----------------+----------------------------------+--------------------------------------+
| BETWEEN_TIMES   | `start_time`, `end_time`         | Between `start_time` and `end_time`. |
+-----------------+----------------------------------+--------------------------------------+

.. _metric-paths:

Metric Paths
^^^^^^^^^^^^

Metric paths are specified as a set of path components delimited by the pipe character ('|'). Here are some examples
of valid metric paths::

    Overall Application Performance|Calls per Minute
    Application Infrastructure Performance|mytier1|Hardware Resources|CPU|%Busy
    Business Transaction Performance|Business Transactions|mytier1|*|Average Response Time (ms)

Note that the last path above contains a wildcard, and will retrieve the Average Response Time for every BT in
the `mytier1` tier. The wildcard character '*' can be subtituted for any component in the path.

To find the path to a particular metric, use the Metric Browser in AppDynamics to drill down to the metric you want,
then right-click and select "Copy Full Path" and paste it into your Python script.


Examples
--------

Connect to a controller and print the list of applications:
    >>> from appd.request import AppDynamicsClient
    >>> c = AppDynamicsClient('http://localhost:8090')
    >>> for app in c.get_applications(): 
    ...     print app.id, app.name
    ...
    2 ACME Book Store
    4 Bundy Online Shoes
    5 Movie Search

Show the controller's configuration:
    >>> for var in c.get_config():
    ...     print var.name, '=', var.value
    ...
    node.permanent.deletion.period = 720
    backend.config.resolution.interval = 0
    metrics.buffer.size = 300
    async.thread.tracking.registration.limit = 2000
    events.upload.limit.per.min = 500

Convert the current date/time to an AppDynamics timestamp:
    >>> from datetime import datetime
    >>> from appd.request import to_ts
    >>> print to_ts(datetime.now())
    1393367892000

Retrieve some application metrics:
    >>> md = c.get_metrics('Overall Application Performance|Average Response Time (ms)', 4,
                           'BEFORE_NOW', duration_in_mins=15, rollup=True)
    >>> mv = md[0].values[0]
    >>> dt = from_ts(mv.start_time_ms)
    >>> 'At {0} the average response time was {1} ms.'.format(dt, mv.value)
    'At 2014-02-25 20:05:00 the average response time was 110 ms.'

Get a list of snapshots taken in the last 15 minutes for slow transactions::
    >>> snaps = c.get_snapshots(9, 'BEFORE_NOW', 15, user_experience='SLOW', need_exit_calls=True)
    >>> len(snaps)
    420
    >>> snaps[0].summary
    u'Request was slower than the average by one of the thresholds below - '
