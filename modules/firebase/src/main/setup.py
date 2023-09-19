#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: setup.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import pathlib

import setuptools

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# The version of the package
VERSION = (HERE / "firebase/.version").read_text().strip()

# The package requirements
REQUIREMENTS = list(filter(None, (HERE / "requirements.txt").read_text().splitlines()))

# This call to setup() does all the work
setuptools.setup(
    name='hspylib-firebase',
    version=VERSION,
    description='HomeSetup - Firebase integration',
    author='Hugo Saporetti Junior',
    author_email='yorevs@hotmail.com',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/yorevs/hspylib',
    project_urls={
        'GitHub': 'https://github.com/yorevs/hspylib',
        'PyPi': 'https://pypi.org/project/hspylib-firebase/'
    },
    license='MIT',
    license_files='LICENSE.md',
    packages=setuptools.find_namespace_packages(),
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix"

    ],
    python_requires='>=3.7',
    install_requires=REQUIREMENTS,
    keywords='firebase,google,integration,application',
    platforms='Darwin,Linux'
)
