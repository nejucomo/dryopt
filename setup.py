#! /usr/bin/env python

import sys
import subprocess
from setuptools import setup, find_packages, Command


PKGNAME = 'dryopt'


def main():
    if 'upload' in sys.argv:
        if '--sign' not in sys.argv and sys.argv[1:] != ['upload', '--help']:
            raise SystemExit('Refusing to upload unsigned packages.')


    setup(name = PKGNAME,
          description = "Don't Repeat Yourself option parsing.",
          url = 'https://github.org/nejucomo/dryopt',
          license = 'GPLv3',
          version = '0.1.dev0', # Make sure this is PEP 440 compliant.
          author = 'Nathan Wilcox',
          author_email = 'nejucomo@gmail.com',
          packages = find_packages(),
          install_requires = [],

          cmdclass = {
            "test_pyflakes": TestPyflakes,
            },
          )


class TestPyflakes (Command):
    """Run pyflakes."""

    description = 'Run pyflakes.'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        status = subprocess.call(['pyflakes', PKGNAME])
        if status != 0:
            raise SystemExit(status)



if __name__ == '__main__':
    main()
