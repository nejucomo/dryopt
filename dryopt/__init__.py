'''dryopt - Don't Repeat Yourself Option parsing.

A quick example:

>>> from dryopt import Command
>>> @Command
>>> def print_greeting(name):
...     """Print a greeting."""
...     print 'Hello, ' + name
...

We can call this function as expected from python:

>>> print_greeting('Ada')
Hello, Ada


We can also easily expose this function as the behavior of a script.
For example, consider a "greeting.py" file with these contents:

  #!/usr/bin/env python

  from dryopt import Command

  @Command
  def print_greeting(name):
      print 'Hello, ' + name

  if __name__ == '__main__':
      print_greeting.call_from_sysargv()


Now if that file is executable, we can invoke it from the commandline:

  $ ./greeting.py Bao
  Hello, Bao


We also have the standard help:

  $ ./greeting.py --help
  usage: greeting.py [-h] name

  Print a greeting.

  positional arguments:
    name

  optional arguments:
    -h, --help  show this help message and exit


Meanwhile, we can import and call the module naturally from python:

  $ python -c 'import greeting; greeting.print_greeting("Cornelius")'
  Hello, Cornelius


Code can concisely define defaults, types, help strings and most argparse
option parsing features for a function decorated by `Command` by declaring
the parameter defaults to be instances of `Option`:

>>> from dryopt import Command, Option
>>> @Command
>>> def print_greeting(
...         name = Option(default = 'Anonymous', help='The name to greet.'),
...         ):
...     """Print a greeting."""
...     print 'Hello, ' + name
...
>>> print_greeting('Ada')
Hello, Ada


The `Command` decorator adapts the function so that it can be called
"naturally" from python.  So for example, if called without arguments,
the `Option` `default` value is passed:

>>> print_greeting()
Hello, Anonymous


Meanwhile, if we put the above definition of `print_greeting` into the
`greeting.py`, then the help output would now look like this:

  $ ./greeting.py --help
  usage: greeting.py [-h] [name]

  Print a greeting.

  positional arguments:
    name        The name to greet.

  optional arguments:
    -h, --help  show this help message and exit


For more details on how to specify `Options` see the docstring for
dryopt.option.

There is also support for scripts which have "subcommands" where the
dryopt-style definition is a decorated class.  See the docstring for
dryopt.command for the API.
'''
