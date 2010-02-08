# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

import mgi.load
import go.load
import uniprot.load
import locatedb.load
import esldb.load

go.load.load()
mgi.load.load()
uniprot.load.load()
locatedb.load.load()
esldb.load.load()
