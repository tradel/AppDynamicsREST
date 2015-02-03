Title:       Python SDK for AppDynamics REST API
Author:      Todd Radel  
Affiliation: AppDynamics Inc.
Email:       tradel@appdynamics.com  
Date:        26 August 2013  

# Python SDK for AppDynamics REST API

Current version: 0.3.0-dev

## Purpose

[AppDynamics](http://www.appdynamics.com) provides a REST interface from which you can pull lots 
of useful data from your controller: metrics like average response time and calls per minute, as well
as metadata like a list of all the detected business transactions. Mostly this involves making 
repeated HTTP calls to the controller, then parsing the results as XML or JSON. 

I set out to create a simple Python library to hide most of the grunt work and complexity.

This library works with both on-premise and SaaS controllers.


## Usage

Here's a simple example. It retrieves a list of business applications from the controller
and prints them out. It uses a helper class `appd.cmdline` to let you supply the controller
URL, username, password, and account on the command line.

``` python
from appd.cmdline import parse_argv
from appd.request import AppDynamicsClient

args = parse_argv()
c = AppDynamicsClient(args.url, args.username, args.password, args.account, args.verbose)
for app in c.get_applications():
	print app.name, app.id
```

## Prerequisites

This package requires a couple of other modules:

* [tzlocal](https://pypi.python.org/pypi/tzlocal)
* [requests](https://pypi.python.org/pypi/requests)
* [lxml](https://pypi.python.org/pypi/lxml)

If you use the setup script documented in the next section, you don't need to install these yourself.
The script will check for the prerequisites and install them if they are missing.


## Installation

The package includes the standard python `setup.py`, so you can install it with a simple command:

``` bash
python setup.py install
```

## Examples

The package includes a couple of scripts that demonstrate what you can do with the REST API:

- **sample.py** - retrieves a list of applications from the controller, then overall application metrics
  and prints them out.
- **license_report_to_csv.py** - generates a CSV report of licenses in use by license type (Java, .NET, PHP,
  and machine-agent-only) which can be imported into Excel.
- **bt_metrics.py** - generates an XML report of metrics by business transaction, similar to the standard data in
  the Business Transactions dashboard. There is an associated XML schema in `xsd/bt_metrics.xsd`.
- **backend_metrics.py** - generates an XML report of metrics for each discovered backend. There is an associated
  XML schema in `xsd/backend_metrics.xsd`.

To run the scripts, you need to pass the controller URL, username, and password on the command line. If you are on
a multi-tenant controller or hosted on SaaS, you will also need to pass an account name. Here's an example:

``` bash
python examples/bt_metrics.py --url http://appdyn-prod.local:8090 --username user1 --password welcome
```

For the full list of command line options supported, see the next section.


## Command Line Options

This package includes a module called `appd.cmdline` that provides a simple command-line parser for use
in your scripts. You're not required to use it, but it allows you to point your script at different controllers
without making any code changes, and if you use it consistently, your scripts will all have a common
command-line syntax, which is nice. It supports the following options:

- **-c** or **--url** for the controller URL. Required.
- **-a** or **--account** for the account name. Optional and defaults to "customer1", which is the account
  name on single-tenant controllers.
- **-u** or **--username** for the user name. Required.
- **-p** or **--password** for the password. Required.
- **-v** or **--verbose** will print out the URLs before they are retrieved.
- **-h** or **--help** will display a summary of the command line options.

The example scripts all use the parser, so you can look at their source to see how to use it.


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


## References

1. [AppDynamics REST API](http://docs.appdynamics.com/display/PRO12S/Use+the+AppDynamics+REST+API)
   page in the official documentation.

