# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from sqlalchemy.orm.session import Session

import waldo.mgi.load
import waldo.go.load
import waldo.goslim.load
import waldo.uniprot.load
import waldo.locate.load
import waldo.hpa.load
import waldo.sequences.load
import waldo.nog.load
import waldo.refseq.load
modules = [
    waldo.go.load,
    waldo.mgi.load,
    waldo.uniprot.load,
    waldo.locate.load,
    waldo.hpa.load,
    waldo.goslim.load,
    waldo.sequences.load,
    waldo.nog.load,
    waldo.refseq.load
    ]

session = waldo.backend.create_session()
c = session.connection()

# These are only valid for SQLite3, but it makes it much faster
c.execute('PRAGMA synchronous=OFF;')
c.execute('PRAGMA journal_mode=OFF;')
for module in modules:
    module.load(create_session=(lambda: Session(bind=c)))
    session.commit()

