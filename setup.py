#! /usr/bin/env python

import os
import sys
import doctest
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
            # Make the usage string for "test" look pretty:
            'test': AbstractTestCommandForDocs,

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


class AbstractTestCommandForDocs (Command):
    """This is just a shim for --help-commands output; the 'test' alias overrides it."""

    description = "Run a full test framework: flake8, unittests, and doctests."



if Flake8Command is None:
    class test_flake8 (Command):
        """Run flake8 tests (requires installing flake8 >= 2.0)."""

        description = __doc__

        user_options = []

        def __init__(self, dist):
            raise SystemExit("You must install flake8 prior to running test_flake8; run:\n\n"
                             "  pip install 'flake8 >= 2.0'\n")

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

    def run(self):
        [pkgname] = self.distribution.packages

        for basedir, _, files in os.walk(pkgname):
            for fname in files:
                path = os.path.join(basedir, fname)
                (modpart, ext) = os.path.splitext(path)
                if ext == '.py':
                    modname = modpart.replace(os.path.sep, '.')
                    mod = __import__(modname)
                    print 'doctest %r' % (modname,)
                    doctest.testmod(mod, name=modname, report=True, verbose=False)



if __name__ == '__main__':
    main()
