#! /usr/bin/env python

import sys
from setuptools import setup, find_packages, Command
from setuptools.command import test

try:
    from flake8.main import Flake8Command
except ImportError:
    Flake8Command = None



def main():
    if 'upload' in sys.argv:
        if '--sign' not in sys.argv and sys.argv[1:] != ['upload', '--help']:
            raise SystemExit('Refusing to upload unsigned packages.')


    setup(name = 'dryopt',
          description = "Don't Repeat Yourself option parsing.",
          url = 'https://github.org/nejucomo/dryopt',
          license = 'GPLv3',
          version = '0.1.dev0', # Make sure this is PEP 440 compliant.
          author = 'Nathan Wilcox',
          author_email = 'nejucomo@gmail.com',
          packages = find_packages(),

          # Runtime dependencies:
          install_requires = [],

          cmdclass = {
            # Rename the standard "test" command to "test_unit":
            'test_unit': test.test,

            # Rename the standard "test" command to "test_unit":
            'test_flake8': test_flake8,

            # Add our test_doc command:
            'test_doc': test_doc,
            },

          command_options = {
            'aliases': {
                # Our test command runs flake8, then unittests, then doctests:
                'test': ('setup.py', 'test_flake8 test_unit test_doc'),
                },
            }
          )


if Flake8Command is None:
    class test_flake8 (Command):
        """Run flake8 tests (requires installing flake8 >= 2.0)."""

        description = __doc__

        user_options = []

        def __init__(self, dist):
            raise SystemExit('You must install flake8 >= 2.0 prior to running test_flake8')

else:
    class test_flake8 (Flake8Command):
        """Run flake8 tests (requires installing flake8 >= 2.0)."""

        def run(self):
            try:
                Flake8Command.run(self)
            except SystemExit, e:
                if e.args != (0,):
                    raise
                # Otherwise continue running other setup commands such as tests.



class test_doc (Command):
    """Test all docstring examples."""

    description = __doc__

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass



if __name__ == '__main__':
    main()
