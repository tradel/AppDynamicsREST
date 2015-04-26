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

