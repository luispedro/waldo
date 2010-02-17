# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import waldo.backend
from sqlalchemy import and_
from waldo.esldb.models import Entry
from waldo.translations.services import translate

def from_ensembl_peptide_id(ensembl_peptide_id, session=None):
    '''
    name = from_ensembl_peptide_id(ensembl_peptide_id, session={backend.create_session()})

    Convert ensembl_peptide_id to eSLDB identifier.

    Parameters
    ----------
      ensembl_peptide_id : Ensembl peptide ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      uid : eSLDB peptide
    '''
    return translate(ensembl_peptide_id, 'ensembl:protein_id', 'esldb:id', session)

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
    if session is None: session = waldo.backend.create_session()
    entry = session.query(Entry).filter(Entry.esldb_id == id).first()
    
    # eSLDB has several levels of locations: experimental, similarity, and predicted
    # some may be blank, others not. They also need to be split on semi-colons, as
    # can be lengthy
    return [{'type':type, 'value':value} for type, value in entry.annotations]

def retrieve_entry(id, session=None):
    '''
    entry = retrieve_entry(id, session={backend.create_session()})

    Retrieve an Entry object based on its ID

    Parameters
    ----------
      id : eSLDB peptide ID
      session : SQLAlchemy session to use (default: create a new one)

    Returns
    -------
      entry : A models.Entry object
    '''
    if session is None: session = waldo.backend.create_session()
    return session.query(Entry).filter(Entry.esldb_id == id).first()
