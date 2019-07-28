#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'aiohttp'
]

setup_requirements = [ ]

test_requirements = [
    'pytest',
    'pytest-asyncio',
    'pytest-aiohttp'
]

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--log-level=DEBUG']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    author="Nat Burns",
    author_email='nbaccount@burnskids.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description="Library to enable control of Screenly OSE digital signage via REST API.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='screenly_ose',
    name='screenly_ose',
    packages=find_packages(include=['screenly_ose']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
    url='https://github.com/burnnat/screenly_ose',
    version='0.0.3',
    zip_safe=False,
)
