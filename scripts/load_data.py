# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

import waldo.mgi.load
import waldo.go.load
import waldo.uniprot.load
import waldo.locate.load
import waldo.esldb.load

mgi.load.load()
go.load.load()
uniprot.load.load()
locate.load.load()
esldb.load.load()
