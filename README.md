====================================
 AppDynamics REST Client For Python
====================================

```python
from appd.cmdline import parse_argv
from appd.request import AppDynamicsClient

args = parse_argv()
c = AppDynamicsClient(args.url, args.username, args.password, args.account, args.verbose)
for app in c.get_applications():
    print app.name, app.id
'''
