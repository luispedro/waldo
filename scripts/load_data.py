# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution
#
import backend
import mgi.files
import mgi.load
import go.files
import go.load
import uniprot.files
import uniprot.load

create_session = backend.create_session

go.load.load(go.files.inputfilename, create_session)
mgi.load.load(mgi.files.inputfilename, create_session)
uniprot.load.load(uniprot.files.inputfilename, create_session)

