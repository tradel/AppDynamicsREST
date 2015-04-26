## FAQ

**I get errors like `ImportError: No module named appd.cmdline` when I try to run the examples scripts.**

You'll see this if you try to run the example scripts before installing the package into your Python `site-packages`
folder. Either follow the installation instructions above, or set the `PYTHONPATH` environment variable before
running the script, like this:

``` bash
PYTHONPATH=. python examples/bt_metrics.py
```

**I can't seem to get the authentication right. I keep getting `HTTPError: 401 Client Error: Unauthorized`.**

Use the same username, password, and account you use when you log into your controller. If your login screen
only has two fields in it (username and password), then you can omit the account.
