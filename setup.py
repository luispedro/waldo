# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from sys import exit
try:
    import setuptools
except:
    print '''
setuptools not found. Please install it.

On linux, the package is often called python-setuptools'''
    exit(1)

long_description = '''\
Waldo: Where Proteins Are
-------------------------

Waldo tells what everyone already knows.
'''

classifiers = [
'Development Status :: 4 - Beta',
'License :: OSI Approved :: MIT License',
'Operating System :: POSIX',
'Operating System :: OS Independent',
'Programming Language :: Python',
'Topic :: Scientific/Engineering',
'Intended Audience :: Science/Research',
]
install_requires = [
    'sqlalchemy',
    'amara==1.2',
    ]

setuptools.setup(name = 'Waldo',
      version = '0.1',
      description = 'Protein Subcellular Location Information Package',
      long_description = long_description,
      author = 'Luis Pedro Coelho and Shannon Quinn',
      author_email = 'lpc@cmu.edu',
      license = 'MIT',
      platforms = ['Any'],
      classifiers = classifiers,
      url = '',
      packages = setuptools.find_packages(exclude='tests'),
      install_requires=install_requires,
      test_suite = 'nose.collector',
      )

