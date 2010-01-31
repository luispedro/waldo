# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution
#
import backend
import mgi.load
import go.files
import go.load
import uniprot.load

go.load.load(go.files.inputfilename, backend.create_session)
mgi.load.load()
uniprot.load.load()

