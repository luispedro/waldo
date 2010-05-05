# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import waldo.backend
from sqlalchemy import and_
from waldo.hpa.models import Entry
from waldo.translations.services import translate

def from_ensembl_peptide_id(ensembl_peptide_id, session=None):
    '''
    name = from_ensembl_peptide_id(ensembl_peptide_id, session={backend.create_session()})

    Convert ensembl_peptide_id to HPA antibody ID.

    Parameters
    ----------
      ensembl_peptide_id : Ensembl peptide ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      id : HPA antibody
    '''
    return translate(ensembl_peptide_id, 'ensembl:peptide_id', 'hpa:id', session)

def from_ensembl_gene_id(ensembl_gene_id, session=None):
    '''
    name = from_ensembl_gene_id(ensembl_gene_id, session={backend.create_session()})

    Convert ensembl_gene_id to HPA antibody ID.

    Parameters
    ----------
      ensembl_gene_id : Ensembl gene ID
      session : SQLAlchemy session to use (default: call backend.create_session())

    Returns
    -------
      id : HPA antibody
    ''' 
    return translate(ensembl_gene_id, 'ensembl:gene_id', 'hpa:id', session)

def retrieve_location_annotations(id, session=None):
    '''
    locations = retrieve_location_annotations(id, session={backend.create_session()})

    Retrieve HPA location annotations based on HPA identifier

    Parameters
    ----------
      id : HPA antibody ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      locations : A list of locations in the format specified by HPA (loc_*)
    '''
    entry = retrieve_entry(id, session)
    return [location.name for location in entry.locations]

def retrieve_entry(id, session=None):
    '''
    entry = retrieve_entry(id, session={backend.create_session()})

    Retrieve an Entry object based on its ID

    Parameters
    ----------
      id : HPA antibody ID
      session : SQLAlchemy session to use (default: create a new one)

    Returns
    -------
      entry : A models.Entry object
    '''
    if session is None: session = waldo.backend.create_session()
    return session.query(Entry).filter(Entry.hpa_id == id).first()


def gen_url(id):
    '''
    url = gen_url(id)

    Generate URL for HPA antibody id `id`

    Parameters
    ----------
      id : HPA antibody id
    Returns
    -------
      url : web url of corresponding data page.
    '''
    return 'http://proteinatlas.org/tissue_profile.php?antibody_id=' + id[-4:]

