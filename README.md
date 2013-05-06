====================================
 AppDynamics REST Client For Python
====================================

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

TODO
====
- [ ] Add support for POST requests (mark node historical, code deployment event, etc.)
