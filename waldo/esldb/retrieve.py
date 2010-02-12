# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import backend
from sqlalchemy import and_
from esldb.models import Entry
from translations.services import translate

def from_ensembl_gene_id(ensembl_gene_id, session=None):
    '''
    name = from_ensembl_gene_id(ensembl_gene_id, session={backend.create_session()})

    Convert ensembl_gene_id to eSLDB identifier.

    Parameters
    ----------
      ensembl_gene_id : Ensembl gene ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      uid : eSLDB peptide
    '''
    # FIXME: This must first convert the gene ID to a peptide ID!
    return translate(ensembl_gene_id, 'ensembl:gene_id', 'esldb:id', session)

def retrieve_location_annotations(id, session=None):
    '''
    locations = retrieve_location_annotations(id, session={backend.create_session()})

    Retrieve eSLDB location annotations based on eSLDB identifier

    Parameters
    ----------
      id : eSLDB peptide ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      locations : A list of locations in the format specified by eSLDB
    '''
    if session is None: session = backend.create_session()
    entry = session.query(Entry).filter(Entry.esldb_id == id).first()
    
    # eSLDB has several levels of locations: experimental, similarity, and predicted
    # some may be blank, others not. They also need to be split on semi-colons, as
    # can be lengthy
    
