# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import backend
from sqlalchemy import and_
from locatedb.models import Entry
from translations.services import translate

def from_ensembl_gene_id(ensembl_gene_id, session=None):
    '''
    name = from_ensembl_gene_id(ensembl_gene_id, session={backend.create_session()})

    Convert ensembl_gene_id to LOCATE uid.

    Parameters
    ----------
      ensembl_gene_id : Ensembl gene ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      uid : LOCATE protein identifier
    '''
    return translate(ensembl_gene_id, 'ensembl:gene_id', 'locate:id', session)

def retrieve_go_annotations(id, session=None):
    '''
    go_ids = retrieve_go_annotations(name, session={backend.create_session()})

    Retrieve GO ids by LOCATE identifier.

    Parameters
    ----------
      id = LOCATE protein uid
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      go_ids : list of go terms (of the form "GO:00...")
    '''
    if session is None: session = backend.create_session()
    entry = session.query(Entry).filter(Entry.locate_id == id).first()

    # parse out all the locations: in entr.locations, entr.predictions.location, 
    # entr.references.locations, and entr.annotations.locations
    locations = []
    locations.extend(_extractGO(entry.locations, locations))
    locations.extend(_extractGO([entry.predictions.goid], locations))
    locations.extend(_extractGO(entry.references.locations, locations))
    locations.extend(_extractGO(entry.annotations.locations, locations))
    return locations

def _extractGO(golist, currentlist):
    retval = []
    for location in golist:
        goids = location.goid.split(';')
        for goid in goids:
            if goid not in currentlist:
                retval.append(goid)
    return retval
