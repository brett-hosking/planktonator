#!/usr/bin/env python
""" Planktonator is a computer vision package built for detecting and measuring particles using computer vision
and machine learning in Python.

    - Outputs .tsv files ready to be imported directly into EcoTaxa

"""

from distutils.core import setup
from setuptools import find_packages

DOCLINES = (__doc__ or '').split("\n")
exec(open('planktonator/version.py').read())
setup(name='planktonator',
      version=__version__,
      description=DOCLINES[0],
      long_description="\n".join(DOCLINES[0:]),
      url='http://github.com/brett-hosking/planktonator',
      license='MIT',
      author='brett hosking',
      author_email='wilski@noc.ac.uk',
      install_requires=[
                "tensorflow>=1.12.0",
                "requests>=2.21.0",
                "imageio>=2.5.0",
                "pandas>=0.24.1",
                ],
      packages=find_packages()
      )
