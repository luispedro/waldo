# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import amara
import models
from os import path
from collections import defaultdict
from translations.models import Translation

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../data'))

#_mouse = 'LOCATE_mouse_v6_20081121.xml'
#_human = 'LOCATE_human_v6_20081121.xml'
_mouse = 'LOCATE_mouse_v6_20081121_SMALL.xml'
_human = 'LOCATE_human_v6_20081121_SMALL.xml'

def load(dirname=None, create_session=None):
    '''
    num_entries = load(dirname={data/}, create_session={backend.create_session})

    Load LOCATE database file information into local relational database

    Parameters
    ----------
      dirname : System folder containing database files
      create_session : Callable object which returns an sqlalchemy session

    Returns
    -------
      num_entries : Number of entries loaded into the local database

    References
    ----------
        To download database files:
        http://locate.imb.uq.edu.au/downloads.shtml
    '''
    if dirname is None: dirname = _datadir
    if create_session is None:
        import backend
        create_session = backend.create_session
    session = create_session()

    # load the mouse and human separately
    loaded = _loadfile(path.join(dirname, _mouse), 'mouse', session)
    loaded += _loadfile(path.join(dirname, _human), 'human', session)
    return loaded

def _loadfile(filename, dbtype, session):
    count = 0
    input = file(filename)

    # LOCATE doesn't define a namespace, so we don't need prefix information ?
    for entry in amara.pushbind(input, u'LOCATE_protein'):
        count += 1

        # even though data are listed in the XML schema as being required,
        # in reality this seems not to be the case. The only entry we can take
        # for granted is this one: <protein> ... </protein>

        # add any isoforms that exist
        isoforms = []
        if hasattr(entry, 'transcript'):
            transcript = entry.transcript
            if hasattr(transcript.other_isoforms, 'isoform'):
                isoforms = [Isoform(elem.class_, elem) for elem in transcript.other_isoforms.isoform]

        # check the experimental data section for location information
        images = []
        if hasattr(entry, 'experimental_data'):
            experimental = entry.experimental_data
            if hasattr(experimental, 'locations'):
                images = [Location(loc.goid, loc.tier1, getattr(loc, 'tier2', None), getattr(loc, 'tier3', None)) for loc in experimental.locations.location]

        # go through the annotations
        annots = []
        if hasattr(entry, 'externalannot'):
             annotations = entry.externalannot
             if hasattr(annotations, 'reference'):
                for elem in annotations.reference:
                    locations = [] 
                    if hasattr(elem, 'locations'):
                        locations = [Location(loc.goid, loc.tier1, getattr(loc, 'tier2', None), getattr(loc, 'tier3', None)) for loc in elem.locations.location]
                    annots.append(Annotation(elem.evidence, elem.source[1].source_id, elem.source[1].source_name, elem.source[1].accn))

        # now the subcellular location predictions
        predicts = []
        if hasattr(entry, 'scl_prediction'):
            predictions = entry.scl_prediction
            if hasattr(predictions, 'source'):
                predicts = [Prediction(elem.source_id, elem.method, elem.location, elem.goid, elem.evaluation) for elem in predictions.source]

        # next, the literature citations
        refs = []
        if hasattr(entry, 'literature'):
            literature = entry.literature 
            if hasattr(literature, 'reference'):
                for elem in literature.reference:
                    locations = [Location(loc.goid, loc.tier1, getattr(loc, 'tier2', None), getattr(loc, 'tier3', None)) for loc in elem.locations.location]
                    refs.append(Literature(elem.author, elem.title, elem.citation, elem.source.source_id, elem.source.source_name, elem.source.accn, locations))
        
        # now the external database references
        extrefs = []
        if hasattr(entry, 'xrefs'):
            xrefs = entry.xrefs
            if hasattr(xrefs, 'xref'):
                for elem in xrefs.xref:
                    extrefs.append(ExternalReference(elem.source.source_id, elem.source.source_name, elem.source.accn))
                    # check if our data is Ensembl-related
                    if elem.source.source_name.startswith('Ensembl'):
                        if elem.source.source_name.startswith('Ensembl-Gene'):
                            subnamespace = 'gene_id'
                        elif elem.source.source_name.startswith('Ensembl-Peptide'):
                            subnamespace = 'peptide_id'
                        t = Translation('ensembl:' + subnamespace, elem.source.accn, 'locate:id', entry.uid)
                        session.add(t)

        # create the object we're really interested in
        protein = entry.protein
        locate_entry = Entry(entry.uid, protein.source.source_name, protein.source_id, protein.accn, isoforms, predicts, refs, annots, images, extrefs, dbtype)
        session.add(locate_entry)

        # finally
        session.commit()
    return count
