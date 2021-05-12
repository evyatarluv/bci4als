#!/usr/bin/env python

"""The setup script."""

# Package meta-data.
NAME = 'bci4als'
DESCRIPTION = 'A Complete Motor Imagery Pipeline for ALS'
URL = 'https://github.com/evyatarluv/BCI-4-ALS'
EMAIL = 'noamsi@post.bgu.ac.il'
AUTHOR = 'Noam Siegel & Evyatar Luvaton'
REQUIRES_PYTHON = '>=3.6.0'

import re

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# version recognition
VERSIONFILE = "src/bci4als/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
setup(name=NAME,
      version=verstr,
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=AUTHOR,
      author_email=EMAIL,
      python_requires=REQUIRES_PYTHON,
      url=URL,
      packages=find_packages(exclude=('tests',)),
      package_data={NAME: ['VERSION']},
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ], )
