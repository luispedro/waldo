# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

import waldo.mgi.load
import waldo.go.load
import waldo.uniprot.load
import waldo.locate.load
import waldo.esldb.load
from os import path

# Put to "dev" to set the application in development mode - namely,
# it loads only the small versions of the database files found in the
# "tests/data" folder
#MODE = 'dev'
MODE = 'testing'

_basedir = path.dirname(path.abspath(__file__))
_testdir = None

if MODE is 'dev':
    _testdir = path.abspath(path.join(_basedir, 'tests/data'))

waldo.go.load.load(_testdir)
waldo.mgi.load.load(_testdir)
waldo.uniprot.load.load(_testdir)
waldo.locate.load.load(_testdir)
waldo.esldb.load.load(_testdir)
