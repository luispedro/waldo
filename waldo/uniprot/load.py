# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
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
from lxml import etree
import re
import models
from os import path
import gzip

import waldo.go
from waldo.translations.models import Translation

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))
_inputfilename = 'uniprot_sprot.xml.gz'
_p = '{http://uniprot.org/uniprot}'

def load(dirname=None, create_session=None, organism_set=set([u'Mus musculus'])):
    '''
    nr_loaded = load(dirname={data/}, create_session={backend.create_session})

    Load uniprot XML into database

    Parameters
    ----------
      dirname : Directory containing the XML Uniprot file
      create_session : a callable object that returns an sqlalchemy session
    Returns
    -------
      nr_loaded : Nr. of entries loaded
    '''
    if dirname is None: dirname = _datadir
    filename = path.join(dirname, _inputfilename)
    if create_session is None:
        from waldo import backend
        create_session = backend.create_session
    session = create_session()
    if filename.endswith('.gz'):
        input = gzip.GzipFile(filename)
    else:
        input = file(filename)
    loaded = 0

    for event, element in etree.iterparse(input, tag=_p+'entry'):
        organisms = []
        for item in element.iterchildren(_p+'organism'):
            for subitem in item.iterchildren():
                if subitem.get('type') == u'scientific':
                    organisms.append(unicode(subitem.text))

        organisms = list(set(organisms) & organism_set)
        if(len(organisms) == 0):
            continue

        accessions = [unicode(acc.text) for acc in element.iterchildren(_p+'accession')]
        name = unicode(element.findtext(_p+'name'))
        sequence = unicode(element.findtext(_p+'sequence'))
        comments = [models.Comment(c.get('type'), unicode(c.findtext(_p+'text'))) for c in element.iterchildren(_p+'comment')]
        references = []
        go_annotations = []

        for ref in element.iterchildren(_p+'reference'):
            for subel in ref.iterchildren():
                #if(subel.tag == _p+'key'):
                #    key = subel.text
                if(subel.tag == _p+'citation'):
                    key = ref.get('key')
                    type = subel.get('type')
                    title = subel.findtext(_p+'title')
                    if(title == None or key == None):
                        continue
                    authors = []
                    for author in subel.iterchildren(_p+'authorList'):
                        authors.extend([person.get('name') for person in author.findall(_p+'person')])
                    authors = " AND ".join(authors)

                    dbrefs = filter(lambda x : x.get('type') == 'DOI', subel.findall(_p+'dbReference'))
                    dbRefString = ''
                    if(len(dbrefs) != 0):
                        dbRefString = "%s:%s" % (dbrefs[0].get('type'), dbrefs[0].get('id'))
                    else:
                        dbrefs = filter(lambda x : x.get('type') == 'PubMed', subel.findall(_p+'dbReference'))
                        if(len(dbrefs) != 0):
                            dbRefString = "%s:%s" % (dbrefs[0].get('type'), dbrefs[0].get('id'))
                    references.append(models.Reference(key, type, title, authors, dbRefString))

        for dbref in element.iterchildren(_p+'dbReference'):
            if dbref.get('type') == 'Ensembl':
                t = Translation('ensembl:transcript_id', dbref.get('id'), 'uniprot:name', name)
                session.add(t)
                t = Translation('uniprot:name', name, 'ensembl:transcript_id', dbref.get('id'))
                session.add(t)
                for prop in dbref.findall(_p+'property'):
                    if prop.get('type') == 'gene designation':
                        subnamespace = 'gene_id'
                    elif prop.get('type') == 'protein sequence ID':
                        subnamespace = 'peptide_id'
                    else:
                        continue
                    t = Translation('ensembl:%s' % subnamespace, prop.get('value'), 'uniprot:name', name)
                    session.add(t)
                    t = Translation('uniprot:name', name, 'ensembl:%s' % subnamespace, prop.get('value'))
                    session.add(t)
            elif dbref.get('type') == 'Go':
                id = dbref.get('id')
                evidence_code = ''
                for prop in dbref.findall(_p+'property'):
                    if prop.get('type') == 'evidence':
                        evidence_code = prop.get('value');

                if waldo.go.is_cellular_component(id):
                    go_annotations.append(models.GoAnnotation(id, evidence_code))

        element.clear()
        while element.getprevious() is not None:
            del element.getparent()[0]

        for acc in accessions:
            session.add(Translation(
                            'uniprot:accession',
                            acc,
                            'uniprot:name',
                            name))
        entry = models.Entry(name, accessions, comments, references, go_annotations, sequence, organisms)
        session.add(entry)
        loaded += 1
        session.commit()
    return loaded
