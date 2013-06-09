# -*- coding: utf-8 -*-
# Copyright (C) 2009-2013, Luis Pedro Coelho <luis@luispedro.org>
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

long_description = file('README.rst').read()

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
    'lxml',
    ]

package_dir = {
    'waldo.tests': 'waldo/tests',
}
package_data = {
    'woof': ['templates/*.html', 'templates/static/*.html', 'media/css/*.css'],
    'waldo.tests': ['data/*'],
}

setuptools.setup(name = 'waldo',
      version = '0.1',
      description = 'Protein Subcellular Location Information Package',
      long_description = long_description,
      author = 'Luis Pedro Coelho and others (See AUTHORS.txt file)',
      author_email = 'luis@luispedro.org',
      license = 'MIT',
      platforms = ['Any'],
      classifiers = classifiers,
      url = 'http://murphylab.web.cmu.edu/services/waldo/home',
      packages = setuptools.find_packages(),
      install_requires = install_requires,
      package_dir = package_dir,
      package_data = package_data,
      scripts = ['bin/update-waldo'],
      test_suite = 'nose.collector',
      )

