# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import waldo.backend
from sqlalchemy import and_
from waldo.uniprot.models import Entry
from waldo.translations.services import translate

def from_ensembl_gene_id(ensembl_gene_id, session=None):
    '''
    name = from_ensembl_gene_id(ensembl_gene_id, session={backend.create_session()})

    Convert ensembl_gene_id to uniprot name (uniprot ID).

    Parameters
    ----------
      ensembl_gene_id : Ensembl gene ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      name : uniprot gene name
    '''
    return translate(ensembl_gene_id, 'ensembl:gene_id', 'uniprot:name', session)

def retrieve_go_annotations(name, session=None):
    '''
    go_ids = retrieve_go_annotations(name, session={backend.create_session()})

    Retrieve GO ids by uniprot name.

    Parameters
    ----------
      name : uniprot name
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      go_ids : list of go terms (of the form "GO:00...")
    '''
    if session is None: session = waldo.backend.create_session()
    entr = session.query(Entry).filter(Entry.name == name).first()
    return [go.go_id for go in entr.go_annotations]

def retrieve_entry(id, session=None):
    '''
    entry = retrieve_entry(id, session={backend.create_session()})

    Retrieve Uniprot entry based on its identifier.

    Parameters
    ----------
      id : Uniprot-specific identifier
      session: SQLAlchemy session to use (default: create a new one)

    Returns
    -------
      entry : models.Entry object
    '''
    if session is None: session = waldo.backend.create_session()
    return session.query(Entry).filter(Entry.name == id).first()
