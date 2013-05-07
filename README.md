====================================
 AppDynamics REST Client For Python
====================================

Purpose
=======

[AppDynamics](http://www.appdynamics.com) provides a REST interface from which you can pull lots 
of useful data from your controller: metrics like average response time and calls per minute, as well
as metadata like a list of all the detected business transactions. Mostly this involves making 
repeated HTTP calls to the controller, then parsing the results as XML or JSON. 

I set out to create a simple Python library to hide most of the grunt work and complexity.

By the way, this works with both on-premise and SaaS controllers.

Usage
=====

Here's an example showing how easy it is to use.

```python
from appd.cmdline import parse_argv
from appd.request import AppDynamicsClient

args = parse_argv()
c = AppDynamicsClient(args.url, args.username, args.password, args.account, args.verbose)
for app in c.get_applications():
    print app.name, app.id
```

Installation
============

The package includes the standard python `setup.py`, so you can install it with any of the usual methods:
* `python setup.py install`
* `easy_install AppDynamicsREST`
* `pip install AppDynamicsREST`

TODO
====
- [ ] Add support for POST requests (mark node historical, code deployment event, etc.)

References
==========
1. [AppDynamics REST API](http://docs.appdynamics.com/display/PRO12S/Use+the+AppDynamics+REST+API)
   page in the official documentation.

