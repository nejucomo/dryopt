#! /usr/bin/env python

import sys
from setuptools import setup, find_packages


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
      install_requires = [],
      )
