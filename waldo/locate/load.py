# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012, Shannon Quinn <squinn@cmu.edu> and Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from lxml import etree
import models
from os import path
from collections import defaultdict
from waldo.translations.models import Translation


_mouse = 'LOCATE_mouse_v6_20081121.xml.zip'
_human = 'LOCATE_human_v6_20081121.xml.zip'

def clear(create_session=None):
    '''
    clear()

    Removes all LOCATE related information
    '''
    from waldo.backend import call_create_session
    session = call_create_session(create_session)
    session.query(models.Isoform).delete()
    session.query(models.Image).delete()
    session.query(models.LocatePrediction).delete()
    session.query(models.Literature).delete()
    session.query(models.LocateAnnotation).delete()
    session.query(models.ExternalReference).delete()
    session.query(models.LocateEntry).delete()
    session.commit()


def load(datadir, create_session=None):
    '''
    num_entries = load(datadir, create_session={backend.create_session})

    Load LOCATE database file information into local relational database

    Parameters
    ----------
    datadir : str
        Path to directory containing database files.
    create_session : callable, optional
        Callable object which returns an sqlalchemy session

    Returns
    -------
    num_entries : int
        Number of entries loaded into the local database

    References
    ----------
    To download database files: http://locate.imb.uq.edu.au/downloads.shtml
    '''
    from waldo.backend import call_create_session
    session = call_create_session(create_session)

    loaded = _loadfile(path.join(datadir, _mouse), 'Mus musculus', session)
    loaded += _loadfile(path.join(datadir, _human), 'Homo sapiens', session)
    return loaded

def _loadfile(filename, organism, session):
    import zipfile
    nr_entries = 0
    zf = zipfile.ZipFile(filename)
    inputf = zf.open(zf.filelist[0])


    def load_image(img, is_coloc):
        return models.Image(
                    img.findtext('filename'),
                    is_coloc,
                    img.findtext('celltype'),
                    img.findtext('magnification'),
                    img.findtext('tag'),
                    img.findtext('epitope'),
                    img.findtext('channel'),
                    img.findtext('channel1'),
                    img.findtext('channel2'),
                    img.findtext('coloc'))

    for _, entry in etree.iterparse(inputf, tag=u'LOCATE_protein'):
        protein_source = None
        name = None
        annots = []
        predicts = []
        refs = []
        extrefs = []
        images = []
        expData = []
        for sub in entry:
            if sub.tag == 'transcript':
                isoforms = [models.Isoform(oi.get('class'), oi.text) for oi in sub.findall('other_isoforms/isoform')]
            elif sub.tag == 'experimental_data':
                expData = [loc.get('goid').split(';') for loc in sub.iterfind('locations/location')]
                for img in sub.iterfind('images/rep_image|images/image'):
                    images.append(load_image(img, False))
                for img in sub.iterfind('coloc_images/rep_coloc_image|coloc_images/coloc_image'):
                    images.append(load_image(img, True))
            elif sub.tag == 'externalannot':
                for annotation in sub.iterfind('reference'):
                    evidence = sub.findtext('evidence')
                    locations = [loc.get('goid').split(';') for loc in sub.iterfind('locations/location')]
                    source = annotation.find('source[1]')
                    for loc in locations:
                        annots.append(models.Annotation(evidence,
                                source.get('source_id'),
                                source.findtext('source_name'),
                                source.findtext('accn'),
                                loc))
            elif sub.tag == 'scl_prediction':
                for source in sub:
                    if source.tag != 'source': continue
                    predicts.append(models.Prediction(
                                        source.get('source_id'),
                                        source.findtext('method'),
                                        source.findtext('location'),
                                        source.findtext('goid')))
            elif sub.tag == 'literature':
                for ref in sub:
                    if ref.tag != 'reference': continue
                    locations = [loc.get('goid').split(';') for loc in sub.iterfind('locations/location')]
                    source = ref.find('source')
                    refs.append(models.Literature(
                                ref.findtext('author'),
                                ref.findtext('title'),
                                ref.findtext('citation'),
                                source.get('source_id'),
                                source.findtext('source_name'),
                                source.findtext('accn'),
                                locations))
            elif sub.tag == 'xrefs':
                for xref in sub.iterfind('xref'):
                    source = xref.find('source')
                    source_name = source.findtext('source_name')
                    accn = source.findtext('accn')
                    extrefs.append(models.ExternalReference(source.get('source_id'), source_name, accn))
                    # check if ref is to Ensembl-*
                    if source_name.startswith('Ensembl'):
                        if source_name.startswith('Ensembl-Gene'):
                            namespace = 'ensembl:gene_id'
                        elif source_name.startswith('Ensembl-Peptide'):
                            namespace = 'ensembl:peptide_id'
                        else:
                            raise IOError('waldo.locate.load: Cannot handle source_name \'%s\'' % source_name)
                        t = Translation(namespace, accn, 'locate:id', entry.get('uid'))
                        session.add(t)
                        t = Translation('locate:id', entry.get('uid'), namespace, accn)
                        session.add(t)
            elif sub.tag == 'protein':
                protein_source = sub.find('source')
                name = sub.findtext('protein_function') # protein_function is what LOCATE calls a human readable name
        session.add(models.Entry(
                        entry.get('uid'),
                        name,
                        isoforms,
                        predicts,
                        refs,
                        annots,
                        expData,
                        images,
                        extrefs,
                        organism))
        nr_entries += 1
        session.commit()

        # We need to cleanup. Otherwise, we end up with so many nodes in memory
        # that that causes a problem.
        entry.clear()
        while entry.getprevious() is not None:
            del entry.getparent()[0]

    return nr_entries
