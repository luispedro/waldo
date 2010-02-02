# -*- coding: utf-8 -*-
# Copyright (C) 2009, Luís Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

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
        protein = entry.protein
        experimental = entry.experimental_data

        # construct the primary Entry object
        # even though other data are listed in the XML schema as being required,
        # in reality this seems not to be the case. The only entry we can take
        # for granted is this one: <protein> ... </protein>
        locate_id = Entry(entry.uid, protein.source.source_name, protein.source_id, protein.accn, dbtype, getattr(protein, 'location_notes', None))
        session.add(locate_id) 

        # add any isoforms that exist
        if hasattr(entry, 'transcript'):
            transcript = entry.transcript
            if hasattr(transcript.other_isoforms, 'isoform'):
                for elem in transcript.other_isoforms.isoform:
                    isoform = Isoform(locate_id.locate_id, elem.class_, elem)
                    session.add(isoform)

        # run through the experimental data
        if hasattr(entry, 'experimental_data'):
            experimental = entry.experimental_data
            if hasattr(experimental.images, 'rep_image'):
                img = experimental.images.rep_image
                image = Image(locate_id.locate_id, False, img.filename, img.celltype, img.magnification, img.tag, img.epitope, img.channel, getattr(img, 'coloc', None), getattr(img, 'channel1', None), getattr(img, 'channel2', None))
                session.add(image)

            if hasattr(experimental.images, 'image'):
                for img in experimental.images.image:
                    image = Image(locate_id.locate_id, False, img.filename, img.celltype, img.magnification, img.tag, img.epitope, img.channel, getattr(img, 'coloc', None), getattr(img, 'channel1', None), getattr(img, 'channel2', None))
                    session.add(image)

            if hasattr(experimental.coloc_images, 'rep_coloc_image'):
                img = experimental.coloc_images.rep_coloc_image
                image = Image(locate_id.locate_id, True, img.filename, img.celltype, img.magnification, img.tag, img.epitope, img.channel, img.coloc, img.channel1, img.channel2)
                session.add(image)

            if hasattr(experimental.coloc_images, 'coloc_image'):
                for img in experimental.coloc_images.coloc_image:
                    image = Image(locate_id.locate_id, True, img.filename, img.celltype, img.magnification, img.tag, img.epitope, img.channel, img.coloc, img.channel1, img.channel2)
                    session.add(image)

            if hasattr(experimental, 'locations'):
                for loc in experimental.locations.location:
                    location = Location(locate_id.locate_id, loc.goid, loc.tier1, None, None, getattr(loc, 'tier2', None), getattr(loc, 'tier3', None))
                    session.add(location)

        # go through the annotations
        if hasattr(entry, 'externalannot'):
             annotations = entry.externalannot
             if hasattr(annotations, 'reference'):
                for elem in annotations.reference:
                    annotation = Annotation(locate_id.locate_id, elem.evidence, elem.source[1].source_id, elem.source[1].source_name, elem.source[1].accn)
                    session.add(annotation)
                    
                    if hasattr(elem, 'locations'):
                        for loc in elem.locations.location:
                            location = Location(locate_id.locate_id, loc.goid, loc.tier1, None, annotation.annot_id, getattr(loc, 'tier2', None), getattr(loc, 'tier3', None))
                            session.add(location)

        # now the subcellular location predictions
        if hasattr(entry, 'scl_prediction'):
            predictions = entry.scl_prediction
            if hasattr(predictions, 'source'):
                for elem in predictions.source:
                    prediction = Prediction(locate_id.locate_id, elem.source_id, elem.method, elem.location, elem.goid, elem.evaluation)
                    session.add(prediction)

        # next, the literature citations
        if hasattr(entry, 'literature'):
            literature = entry.literature 
            if hasattr(literature, 'reference'):
                for elem in literature.reference:
                    cite = Literature(locate_id.locate_id, elem.author, elem.title, elem.citation, elem.organism, elem.source.source_id, elem.source.source_name, elem.source.accn, elem.notes)
                    session.add(cite)
                    for loc in elem.locations.location:
                        location = Location(locate_id.locate_id, loc.goid, loc.tier1, cite.ref_id, None, getattr(loc, 'tier2', None), getattr(loc, 'tier3', None))
                        session.add(location)
        
        # now the external database references
        if hasattr(entry, 'xrefs'):
            xrefs = entry.xrefs
            if hasattr(xrefs, 'xref'):
                for elem in xrefs.xref:
                    xref = ExternalDatabase(locate_id.locate_id, elem.source.source_id, elem.source.source_name, elem.source.accn)
                    session.add(xref)

        # finally
        session.commit()
    return count
