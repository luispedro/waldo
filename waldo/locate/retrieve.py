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
    for location in entry.locations:
        locations.extend(_splitGO(location, locations)) 

    for predict in entry.predictions:
        locations.extend(_splitGO(predict.goid, locations))

    for reference in entry.references:
        for location in reference.locations:
            locations.extend(_splitGO(location.goid, locations))

    for annotation in entry.annotations:
        for location in annotation.locations:
            locations.extend(_splitGO(location.goid, locations))

    return locations

def _splitGO(goids, curlist):
    retval = []
    ids = goids.split(';')
    for goid in ids:
        if goid not in curlist: retval.append(goid)
    return list(set(retval))

def _extractGO(elemlist, currentlist):
    retval = []
    for elem in elemlist:
        for location in elem.locations:
            goids = location.goid.split(';')
            for goid in goids:
                if goid not in currentlist:
                    retval.append(goid)
    return retval
