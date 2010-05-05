# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from sqlalchemy import and_
from waldo import backend
from waldo.locate.models import Entry
from waldo.translations.services import translate
from waldo.go.go import id_to_term

def from_ensembl_gene_id(ensembl_gene_id, session=None):
    '''
    locate_id = from_ensembl_gene_id(ensembl_gene_id, session={backend.create_session()})

    Convert ensembl_gene_id to LOCATE uid.

    Parameters
    ----------
      ensembl_gene_id : Ensembl gene ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      locate_id : LOCATE protein identifier
    '''
    return translate(ensembl_gene_id, 'ensembl:gene_id', 'locate:id', session)

def from_ensembl_peptide_id(ensembl_peptide_id, session=None):
    '''
    locate_id = from_ensembl_peptide_id(ensembl_peptide_id, session={backend.create_session()})

    Convert ensembl_peptide_id to LOCATE uid.

    Parameters
    ----------
      ensembl_peptide_id : Ensembl peptide ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      locate_id : LOCATE protein identifier
    '''
    return translate(ensembl_peptide_id, 'ensembl:peptide_id', 'locate:id', session)

def _splitGO(goids):
    goids = goids.split(';')
    goids = map(id_to_term, goids)
    return goids

def retrieve_go_annotations(id, session=None):
    '''
    go_ids = retrieve_go_annotations(name, session={backend.create_session()})

    Retrieve GO ids by LOCATE identifier.

    Parameters
    ----------
      id : LOCATE protein uid
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      go_ids : list of go terms (of the form "GO:00...")
    '''
    if session is None: session = backend.create_session()
    entry = session.query(Entry).filter(Entry.id == id).first()

    locations = set()
    for location in entry.locations:
        locations.update(_splitGO(location.goid))

    for predict in entry.predictions:
        locations.update(_splitGO(predict.goid))

    for reference in entry.references:
        for location in reference.locations:
            locations.update(_splitGO(location.goid))

    for annotation in entry.annotations:
        for location in annotation.locations:
            locations.update(_splitGO(location.goid))

    return list(locations)

def retrieve_entry(id, session=None):
    '''
    entry = retrieve_entry(id, session={backend.create_session()})

    Retrieve an Entry object based on its ID

    Parameters
    ----------
      id : LOCATE database ID
      session : SQLAlchemy session to use (default: create a new one)

    Returns
    -------
      entry : A models.Entry object
    '''
    if session is None: session = backend.create_session()
    return session.query(Entry).filter(Entry.id == id).first()


