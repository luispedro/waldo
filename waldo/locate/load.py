# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import amara
import models
from os import path
from collections import defaultdict
from waldo.translations.models import Translation

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))

_mouse = 'LOCATE_mouse_v6_20081121.xml'
_human = 'LOCATE_human_v6_20081121.xml'

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
        import waldo.backend
        create_session = waldo.backend.create_session
    session = create_session()

    # load the mouse and human separately
    loaded = _loadfile(path.join(dirname, _mouse), 'Mus musculus', session)
    loaded += _loadfile(path.join(dirname, _human), 'Homo sapiens', session)
    return loaded

def _loadfile(filename, dbtype, session):
    count = 0
    input = file(filename)

    # LOCATE doesn't define a namespace, so we don't need prefix information ?
    for entry in amara.pushbind(input, u'LOCATE_protein'):
        count += 1

        # even though data are listed in the XML schema as being required,
        # in reality this seems not to be the case. As such, many checks are
        # in place to make sure certain attributes do exist

        # add any isoforms that exist
        isoforms = []
        if hasattr(entry, 'transcript'):
            transcript = entry.transcript
            if hasattr(transcript.other_isoforms, 'isoform'):
                isoforms = [models.Isoform(elem.class_, str(elem)) for elem in transcript.other_isoforms.isoform]

        # check the experimental data section for location information
        images = []
        expData = []
        if hasattr(entry, 'experimental_data'):
            experimental = entry.experimental_data
            if hasattr(experimental, 'locations'):
                expData = [models.Location(loc.goid, getattr(loc, 'tier1', None), getattr(loc, 'tier2', None), getattr(loc, 'tier3', None)) for loc in experimental.locations.location]
            # also load the image data
            reg_images = experimental.images
            coloc_images = experimental.coloc_images
            # are there any images?
            if hasattr(reg_images, 'rep_image'):
                img = reg_images.rep_image
                images.append(models.Image(str(img.filename), False, str(img.celltype), str(img.magnification), str(img.tag), str(img.epitope), str(img.channel), str(getattr(img, 'channel1', None)), str(getattr(img, 'channel2', None)), str(img.coloc)))
            if hasattr(reg_images, 'image'):
                for img in reg_images.image:
                    images.append(models.Image(str(img.filename), False, str(img.celltype), str(img.magnification), str(img.tag), str(img.epitope), str(img.channel), str(getattr(img, 'channel1', None)), str(getattr(img, 'channel2', None)), str(img.coloc)))
            if hasattr(coloc_images, 'rep_coloc_image'):
                img = coloc_images.rep_coloc_image
                images.append(models.Image(str(img.filename), True, str(img.celltype), str(img.magnification), str(img.tag), str(img.epitope), str(img.channel), str(getattr(img, 'channel1', None)), str(getattr(img, 'channel2', None)), str(img.coloc)))
            if hasattr(coloc_images, 'coloc_image'):
                for img in coloc_images.coloc_image:
                    images.append(models.Image(str(img.filename), True, str(img.celltype), str(img.magnification), str(img.tag), str(img.epitope), str(img.channel), str(getattr(img, 'channel1', None)), str(getattr(img, 'channel2', None)), str(img.coloc)))

        # go through the annotations
        annots = []
        if hasattr(entry, 'externalannot'):
             annotations = entry.externalannot
             if hasattr(annotations, 'reference'):
                for elem in annotations.reference:
                    locations = [] 
                    if hasattr(elem, 'locations'):
                        locations = [models.Location(loc.goid, getattr(loc, 'tier1', None), getattr(loc, 'tier2', None), getattr(loc, 'tier3', None)) for loc in elem.locations.location]
                    annots.append(models.Annotation(str(elem.evidence), elem.source[1].source_id, str(elem.source[1].source_name), str(elem.source[1].accn), locations))

        # now the subcellular location predictions
        predicts = []
        if hasattr(entry, 'scl_prediction'):
            predictions = entry.scl_prediction
            if hasattr(predictions, 'source'):
                try:
                    predicts = [models.Prediction(elem.source_id, str(elem.method), str(elem.location), str(elem.goid)) for elem in predictions.source]
                except AttributeError:
                    pass
                    # thankfully, we don't care in this situation

        # next, the literature citations
        refs = []
        if hasattr(entry, 'literature'):
            literature = entry.literature 
            if hasattr(literature, 'reference'):
                for elem in literature.reference:
                    locations = [models.Location(loc.goid, getattr(loc, 'tier1', None), getattr(loc, 'tier2', None), getattr(loc, 'tier3', None)) for loc in elem.locations.location]
                    refs.append(models.Literature(str(elem.author), str(elem.title), str(elem.citation), elem.source.source_id, str(elem.source.source_name), str(elem.source.accn), locations))
        
        # now the external database references
        extrefs = []
        if hasattr(entry, 'xrefs'):
            xrefs = entry.xrefs
            if hasattr(xrefs, 'xref'):
                for elem in xrefs.xref:
                    extrefs.append(models.ExternalReference(elem.source.source_id, str(elem.source.source_name), str(elem.source.accn)))
                    # check if our data is Ensembl-related
                    value = str(elem.source.source_name)
                    if value.startswith('Ensembl'):
                        if value.startswith('Ensembl-Gene'):
                            subnamespace = 'gene_id'
                        elif value.startswith('Ensembl-Peptide'):
                            subnamespace = 'peptide_id'
                        t = Translation('ensembl:' + subnamespace, str(elem.source.accn), 'locate:id', entry.uid)
                        session.add(t)
                        t = Translation('locate:id', entry.uid, 'ensembl:%s' % subnamespace, str(elem.source.accn))
                        session.add(t)

        # create the object we're really interested in
        protein = entry.protein
        locate_entry = models.Entry(entry.uid, str(protein.source.source_name), protein.source.source_id, str(protein.source.accn), isoforms, predicts, refs, annots, expData, images, extrefs, dbtype)
        session.add(locate_entry)

        # finally
        session.commit()
    return count
