#! /usr/bin/env python

import sys
from setuptools import setup, find_packages, Command
from setuptools.command import test



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

          # dev-time dependencies:
          setup_requires = ['flake8 >= 2.0'],

          cmdclass = {
            # Rename the standard "test" command to "test_unit":
            'test_unit': test.test,

            # Add our test_doc command:
            'test_doc': test_doc,
            },

          command_options = {
            'aliases': {
                # Our test command runs flake8, then unittests, then doctests:
                'test': ('setup.py', 'test_flake8 test_unit test_doc'),

                # Rename the "flake8" command to "test_flake8"
                'test_flake8': ('setup.py', 'flake8'),
                },
            }
          )


class test_doc (Command):
    """A distutils command to run doctests on all modules."""

    description = 'Test all docstring examples.'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass



if __name__ == '__main__':
    main()
