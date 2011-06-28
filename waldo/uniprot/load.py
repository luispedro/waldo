# -*- coding: utf-8 -*-
# Copyright (C) 2009-2011, Luis Pedro Coelho <lpc@cmu.edu>
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
import models
from os import path
import gzip

import waldo.go
from waldo.translations.models import Translation

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))
_inputfilename = 'uniprot_sprot.xml.gz'
_p = '{http://uniprot.org/uniprot}'

def load(dirname=None, create_session=None, organism_set=set([u'Mus musculus', u'Homo Sapiens'])):
    '''
    nr_loaded = load(dirname={data/}, create_session={backend.create_session}, organism_set={'Mus musculus', 'Homo Sapiens'})

    Load uniprot into database

    Parameters
    ----------
    dirname : str, optional
        Directory containing the XML Uniprot file
    create_session : callable, optional
        a callable object that returns an sqlalchemy session
    organism_set : set of str, optional
        If not None, only organisms in this set will be loaded. Defaults to
        ['Mus Musculus', 'Homo Sapiens']

    Returns
    -------
    nr_loaded : int
        Nr. of entries loaded. This double counts entries that are parsed both
        from SwissProt and from the ID mapping.
    '''
    if dirname is None: dirname = _datadir
    if create_session is None:
        from waldo import backend
        create_session = backend.create_session
    session = create_session()
    loaded = _load_uniprot_sprot(dirname, session, organism_set)
    loaded += _load_idmapping(dirname, session, organism_set)
    return loaded


def _load_uniprot_sprot(dirname, session, organism_set):
    input = gzip.GzipFile(path.join(dirname, _inputfilename))
    loaded = 0

    for event, element in etree.iterparse(input, tag=_p+'entry'):
        organisms = []
        for item in element.iterchildren(_p+'organism'):
            for subitem in item.iterchildren():
                if subitem.get('type') == u'scientific':
                    organisms.append(unicode(subitem.text))

        if organism_set is not None:
            if not len(set(organisms) & organism_set):
                continue

        accessions = [unicode(acc.text) for acc in element.iterchildren(_p+'accession')]
        name = unicode(element.findtext(_p+'name'))
        rname = element.find(_p + 'protein').find(_p+'recommendedName').find(_p + 'fullName').text
        sequence = unicode(element.findtext(_p+'sequence'))
        comments = [models.Comment(c.get('type'), unicode(c.findtext(_p+'text'))) for c in element.iterchildren(_p+'comment')]
        references = []
        go_annotations = []

        for ref in element.iterchildren(_p+'reference'):
            for subel in ref.iterchildren():
                if(subel.tag == _p+'citation'):
                    key = ref.get('key')
                    type = subel.get('type')
                    title = subel.findtext(_p+'title')
                    if title is None or key is None:
                        continue
                    authors = []
                    for author in subel.iterchildren(_p+'authorList'):
                        authors.extend([person.get('name') for person in author.findall(_p+'person')])
                    authors = " AND ".join(authors)

                    dbrefs = filter(lambda x : x.get('type') == 'DOI', subel.findall(_p+'dbReference'))
                    dbRefString = ''
                    if len(dbrefs):
                        dbRefString = "%s:%s" % (dbrefs[0].get('type'), dbrefs[0].get('id'))
                    else:
                        dbrefs = filter(lambda x : x.get('type') == 'PubMed', subel.findall(_p+'dbReference'))
                        if len(dbrefs):
                            dbRefString = "%s:%s" % (dbrefs[0].get('type'), dbrefs[0].get('id'))
                    references.append(models.Reference(key, type, title, authors, dbRefString))

        for dbref in element.iterchildren(_p+'dbReference'):
            if dbref.get('type') == 'Go':
                id = dbref.get('id')
                evidence_code = ''
                for prop in dbref.findall(_p+'property'):
                    if prop.get('type') == 'evidence':
                        evidence_code = prop.get('value');
                if waldo.go.is_cellular_component(id, session):
                    go_annotations.append(models.GoAnnotation(id, evidence_code))

        # We need to cleanup. Otherwise, we end up with so many nodes in memory
        # that we run out.
        element.clear()
        while element.getprevious() is not None:
            del element.getparent()[0]

        entry = models.Entry(name, rname, accessions, comments, references, go_annotations, sequence, organisms)
        session.add(entry)
        loaded += 1
        session.commit()
    return loaded

def _ensembl_guess(ensgene):
    if ensgene.startswith('ENSMUS'):
        return u'Mus Musculus'
    return '<unknown>'

def _load_idmapping(dirname, session, organism_set):
    input = gzip.GzipFile(path.join(dirname, 'idmapping_selected.tab.gz'))
    loaded = 0
    seen_IDs = set()
    for line in input:
        UniProtKB_AC, \
            UniProtKB_ID, \
            GeneID_EntrezGene, \
            RefSeq, \
            GI, \
            PDB, \
            GO, \
            IPI, \
            UniRef100, \
            UniRef90, \
            UniRef50, \
            UniParc, \
            PIR, \
            NCBI_taxon, \
            MIM, \
            UniGene, \
            PubMed, \
            EMBL, \
            EMBL_CDS, \
            Ensembl, \
            Ensembl_TRS, \
            Ensembl_PRO, \
            Additional_PubMed = line[:-1].split('\t')
        if organism_set is not None and \
            _ensembl_guess(Ensembl) not in organism_set:
            continue


        session.add(Translation(
                'uniprot:accession',
                UniProtKB_AC,
                'uniprot:name',
                UniProtKB_ID))
        session.add(Translation(
                'uniprot:accession',
                UniProtKB_AC,
                'ensembl:gene_id',
                Ensembl))
        session.add(Translation(
                'uniprot:accession',
                UniProtKB_AC,
                'ensembl:peptide_id',
                Ensembl_PRO))
        if not UniProtKB_ID in seen_IDs:
            session.add(Translation(
                    'uniprot:name',
                    UniProtKB_ID,
                    'ensembl:gene_id',
                    Ensembl))
            session.add(Translation(
                    'uniprot:name',
                    UniProtKB_ID,
                    'ensembl:peptide_id',
                    Ensembl_PRO))
            session.add(Translation(
                    'ensembl:peptide_id',
                    Ensembl_PRO,
                    'uniprot:name',
                    UniProtKB_ID))
            session.add(Translation(
                    'ensembl:gene_id',
                    Ensembl,
                    'uniprot:name',
                    UniProtKB_ID))
            seen_IDs.add(UniProtKB_ID)
        session.commit()
        loaded += 1
    return loaded


