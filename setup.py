#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import ribbon

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

packages = [
    'ribbon',
]

package_data = {
}

requires = [
  'PyYaml'
]

classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='ribbon',
    version=ribbon.__version__,
    description='A generic, configurable omnibus package builder',
    long_description=readme,
    packages=packages,
    package_data=package_data,
    install_requires=requires,
    author=ribbon.__author__,
    author_email='michael@aptira.com',
    url='https://github.com/michaeltchapman/ribbon',
    license='Apache',
    classifiers=classifiers,
    scripts=['bin/ribbon'],
)
