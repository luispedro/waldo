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
import re
import amara
import models
import gzip
from os import path

import waldo.go
from waldo.translations.models import Translation

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))
_inputfilename = 'uniprot_sprot.xml.gz'

def load(dirname=None, create_session=None):
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
    uniprot_nss = { u'uniprot' : u'http://uniprot.org/uniprot', }
    if filename.endswith('.gz'):
        input = gzip.GzipFile(filename)
    else:
        input = file(filename)
    loaded = 0
    for entry in amara.pushbind(input, '//uniprot:entry', prefixes=uniprot_nss):
        accessions = [unicode(acc) for acc in entry.accession]
        name = unicode(entry.name)
        sequence = unicode(entry.sequence)
        comments = [models.Comment(c.type, unicode(c).strip()) for c in getattr(entry, 'comments', [])]
        references = []
        go_annotations = []
        evidence_codes = []

        for ref in entry.reference:
            try:
                key = ref.key
                type = ref.citation.type
                title = unicode(ref.citation.title).strip()
                authors = []
                for p in ref.authorList.person:
                    authors.append(p.name)
                authors = " AND ".join(authors)
                references.append( models.Reference(key, type, title, authors) )
            except AttributeError:
                pass # This means that this was a reference without a title or key, which we don't care about

        for dbref in getattr(entry, 'dbReference', ()):
            if dbref.type == 'Ensembl':
                t = Translation('ensembl:transcript_id', dbref.id, 'uniprot:name', name)
                session.add(t)
                t = Translation('uniprot:name', name, 'ensembl:transcript_id', dbref.id)
                session.add(t)
                for prop in dbref.property:
                    if prop.type == 'gene designation':
                        subnamespace = 'gene_id'
                    elif prop.type == 'protein sequence ID':
                        subnamespace = 'peptide_id'
                    elif prop.type == 'evidence':
                        evidence_codes.append(models.Evidence(prop.value))
                    else:
                        continue
                    t = Translation('ensembl:'+subnamespace, prop.value, 'uniprot:name', name)
                    session.add(t)
                    t = Translation('uniprot:name', name, 'ensembl:%s' % subnamespace, prop.value)
                    session.add(t)
            elif dbref.type == 'Go':
                id = dbref.id
                for prop in dbref.property:
                    if prop.type == 'evidence':
                        evidence_codes.append(models.Evidence(prop.value, id))

                if waldo.go.is_cellular_component(id):
                    go_annotations.append( models.GoAnnotation(id) )
        for acc in accessions:
            session.add(Translation(
                            'uniprot:accession',
                            acc,
                            'uniprot:name',
                            name))
        organisms = []
        for organism in getattr(entry, 'organism', ()):
            for orgname in organism.name:
                if orgname.type == u'scientific':
                    organisms.append(unicode(orgname))
        entry = models.Entry(name, accessions, comments, references, go_annotations, sequence, organisms, evidence_codes)
        session.add(entry)
        loaded += 1
        session.commit()
    return loaded

