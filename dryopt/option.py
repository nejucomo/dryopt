"""Specification for commandline options."""


class Option (object):
    """Represent a commandline Option.

    The arguments are similar to `argparse.Parser.add_argument`, with
    these exceptions:

    * No 'name' keyword is allowed; the name comes from the Command function
      parameter name.

    * No 'default' keyword is allowed; the default comes from the Command
      function parameter default value.

    * No 'nargs' keyword is allowed.

    Here's an example of creating an option manually:

    >>> from dryopt.option import Option
    >>> opt = Option(type=int, help='Some number.')
    >>> opt
    <Option ??? type:int required 'Some number.'>
    >>> opt.initialize('count', default=3)
    <Option count type:int default:3 'Some number.'>
    >>> opt
    <Option count type:int default:3 'Some number.'>
    """
