#!/usr/bin/env python
""" Planktonator is a Python package built for detecting and measuring particles.

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
      author_email='brett.hosking@gmail.com',
      install_requires=[
            "numpy>=1.16.2",
            "imageio>=2.5.0",
            "pandas>=0.24.1",
            "scipy>=1.2.1",
            "scikit-image>=0.14.2"  
                ],
      packages=find_packages()
      )
