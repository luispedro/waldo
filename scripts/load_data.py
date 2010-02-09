# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

import mgi.load
import go.load
import uniprot.load
import locatedb.load
import esldb.load
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

go.load.load(_testdir)
mgi.load.load(_testdir)
uniprot.load.load(_testdir)
locatedb.load.load(_testdir)
esldb.load.load(_testdir)
