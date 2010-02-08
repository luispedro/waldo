# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

import mgi.load
import go.load
import uniprot.load
import esldb.load
import locatedb.load

#go.load.load()
print 'Beginning MGI...'
mgi.load.load()
print 'MGI done.'
#print 'Beginning Uniprot...'
#uniprot.load.load()
#print 'Uniprot done.'
print 'Beginning LOCATE...'
locatedb.load.load()
print 'LOCATE done. Beginning eSLDB...'
esldb.load.load()
print 'eSLDB done. Finished!'
