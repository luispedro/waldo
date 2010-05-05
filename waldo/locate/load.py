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

    loaded = _loadfile(path.join(dirname, _mouse), 'Mus musculus', session)
    loaded += _loadfile(path.join(dirname, _human), 'Homo sapiens', session)
    return loaded

def _loadfile(filename, organism, session):
    from models import Isoform, Image
    count = 0
    input = file(filename)

    # LOCATE doesn't define a namespace, so we don't need prefix information ?
    for entry in amara.pushbind(input, u'LOCATE_protein'):
        count += 1

        # even though data are listed in the XML schema as being required,
        # in reality this seems not to be the case. As such, many checks are
        # in place to make sure certain attributes do exist

        # add any isoforms that exist
        transcript = getattr(entry, 'transcript', None)
        isoforms = [Isoform(elem.class_, str(elem)) for elem in getattr(transcript.other_isoforms, 'isoform', ())]

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
            def _str(obj):
                if obj is None:
                    return None
                return str(obj)
            # are there any images?
            if hasattr(reg_images, 'rep_image'):
                img = reg_images.rep_image
                images.append(Image(str(img.filename), False, str(img.celltype), str(img.magnification), str(img.tag), str(img.epitope), str(img.channel), _str(getattr(img, 'channel1', None)), _str(getattr(img, 'channel2', None)), str(img.coloc)))

            for img in getattr(reg_images, 'image', ()):
                images.append(Image(str(img.filename), False, str(img.celltype), str(img.magnification), str(img.tag), str(img.epitope), str(img.channel), _str(getattr(img, 'channel1', None)), _str(getattr(img, 'channel2', None)), str(img.coloc)))
            if hasattr(coloc_images, 'rep_coloc_image'):
                img = coloc_images.rep_coloc_image
                images.append(Image(str(img.filename), True, str(img.celltype), str(img.magnification), str(img.tag), str(img.epitope), str(img.channel), _str(getattr(img, 'channel1', None)), _str(getattr(img, 'channel2', None)), str(img.coloc)))

            for img in getattr(coloc_images, 'coloc_image', ()):
                images.append(Image(str(img.filename), True, str(img.celltype), str(img.magnification), str(img.tag), str(img.epitope), str(img.channel), _str(getattr(img, 'channel1', None)), _str(getattr(img, 'channel2', None)), str(img.coloc)))

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
            for elem in getattr(entry.xrefs, 'xref', ()):
                extrefs.append(models.ExternalReference(elem.source.source_id, str(elem.source.source_name), str(elem.source.accn)))
                # check if our data is Ensembl-related
                value = str(elem.source.source_name)
                if value.startswith('Ensembl'):
                    if value.startswith('Ensembl-Gene'):
                        namespace = 'ensembl:gene_id'
                    elif value.startswith('Ensembl-Peptide'):
                        namespace = 'ensembl:peptide_id'
                    else:
                        raise IOError('waldo.locate.load: Cannot handle source_name \'%s\'' % value)
                    t = Translation(namespace, str(elem.source.accn), 'locate:id', entry.uid)
                    session.add(t)
                    t = Translation('locate:id', entry.uid, namespace, str(elem.source.accn))
                    session.add(t)

        protein = entry.protein
        locate_entry = models.Entry(entry.uid, str(protein.source.source_name), protein.source.source_id, str(protein.source.accn), isoforms, predicts, refs, annots, expData, images, extrefs, organism)
        session.add(locate_entry)

        session.commit()
    return count
