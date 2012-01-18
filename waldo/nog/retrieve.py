# -*- coding: utf-8 -*-
# Copyright (C) 2011, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from sqlalchemy import and_
from waldo import backend
from waldo.nog.models import NogEntry
from waldo.translations.services import translate

def retrieve_orthologs(ensembl_id, session=None):
    '''
    orthologs = retrieve_orthologs(ensembl_id, session={backend.create_session()})

    Retrieve orthologs by Ensembl peptide id.

    Parameters
    ----------
    ensembl_id : str
        Ensembl Peptide ID
    session : SQLAlchemy session, optional
         to use (default: call backend.create_session())

    Returns
    -------
    orthologs : list of str or None
        List of Ensembl IDs. If the protein is not found, None is returned. If
        the protein is found, but no orthologs are defined, an empty list is
        returned.
    '''
    if session is None: session = backend.create_session()
    entry = session.query(NogEntry).filter(NogEntry.ensembl_peptide == ensembl_id).first()
    if entry is None:
        return None
    entries = session.query(NogEntry).filter(NogEntry.orthologous_group == entry.orthologous_group).all()
    entries = [e.ensembl_peptide for e in entries]
    entries = [e for e in entries if e != ensembl_id]
    return entries
