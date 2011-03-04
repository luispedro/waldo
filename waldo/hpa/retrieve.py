# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import waldo.backend
from sqlalchemy import and_
from waldo.hpa.models import Entry
from waldo.translations.services import translate

def retrieve_location_annotations(id, session=None):
    '''
    locations = retrieve_location_annotations(id, session={backend.create_session()})

    Retrieve location annotations based on Ensembl identifier

    Parameters
    ----------
      id : Ensembl ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      locations : A list of locations
    '''
    entry = retrieve_entry(id, session)
    return [location.name for location in entry.locations]

def retrieve_entry(id, session=None):
    '''
    entry = retrieve_entry(id, session={backend.create_session()})

    Retrieve an Entry object based on its ID

    Parameters
    ----------
      id : Ensembl antibody ID
      session : SQLAlchemy session to use (default: create a new one)

    Returns
    -------
      entry : A models.Entry object
    '''
    if session is None: session = waldo.backend.create_session()
    return session.query(Entry).filter(Entry.ensembl_id == id).first()

def gen_url(id):
    '''
    url = gen_url(id)

    Generate URL for Ensembl antibody id `id`

    Parameters
    ----------
      id : Ensembl antibody id
    Returns
    -------
      url : web url of corresponding data page.
    '''
    return 'http://proteinatlas.org/tissue_profile.php?antibody_id=' + id[-4:]

