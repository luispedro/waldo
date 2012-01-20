# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012, Luis Pedro Coelho <luis@luispedro.org>
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

from waldo.tools import _gzip_open
import waldo.go
from waldo.translations.models import Translation

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))
_inputfilename = 'uniprot_sprot.xml.gz'
_p = '{http://uniprot.org/uniprot}'

def load(dirname=None, create_session=None, organism_set=set([u'Mus musculus', u'Homo sapiens'])):
    '''
    nr_loaded = load(dirname={data/}, create_session={backend.create_session}, organism_set={'Mus musculus', 'Homo sapiens'})

    Load uniprot into database

    Parameters
    ----------
    dirname : str, optional
        Directory containing the XML Uniprot file
    create_session : callable, optional
        a callable object that returns an sqlalchemy session
    organism_set : set of str, optional
        If not None, only organisms in this set will be loaded. Defaults to
        ['Mus musculus', 'Homo sapiens']

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
    loaded += _load_sec_ac(dirname, session)
    return loaded

def _cleanup(element):
    # We need to cleanup. Otherwise, we end up with so many nodes in memory
    # that we run out.
    element.clear()
    while element.getprevious() is not None:
        del element.getparent()[0]

def _load_uniprot_sprot(dirname, session, organism_set):
    input = _gzip_open(path.join(dirname, _inputfilename))
    loaded = 0

    for event, element in etree.iterparse(input, tag=_p+'entry'):
        organisms = []
        for item in element.iterchildren(_p+'organism'):
            for subitem in item.iterchildren():
                if subitem.get('type') == u'scientific':
                    organisms.append(unicode(subitem.text))

        if organism_set is not None:
            if not len(set(organisms) & organism_set):
                _cleanup(element)
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
                go_annotations.append(models.GoAnnotation(id, evidence_code))

        _cleanup(element)

        entry = models.Entry(name, rname, accessions, comments, references, go_annotations, sequence, organisms)
        session.add(entry)
        loaded += 1
        session.commit()
    return loaded

def _name_guess(name):
    if name.endswith('_MOUSE'):
        return u'Mus musculus'
    if name.endswith('_HUMAN'):
        return u'Homo sapiens'
    return '<unknown>'

def _load_idmapping(dirname, session, organism_set):
    def add(input_ns, input_n, output_ns, output_n):
        session.add(Translation(input_ns, input_n, output_ns, output_n))
    input = _gzip_open(path.join(dirname, 'idmapping_selected.tab.gz'))
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
            _name_guess(UniProtKB_ID) not in organism_set:
            continue

        add('uniprot:accession', UniProtKB_AC, 'uniprot:name', UniProtKB_ID)
        add('uniprot:accession', UniProtKB_AC, 'ensembl:gene_id', Ensembl)
        add('uniprot:accession', UniProtKB_AC, 'ensembl:peptide_id', Ensembl_PRO)
        for embl_cds in EMBL_CDS.split('; '):
            add('embl:cds', embl_cds, 'uniprot:name', UniProtKB_ID)
        if not UniProtKB_ID in seen_IDs:
            Ensembl = Ensembl.split('; ')
            Ensembl_PRO = Ensembl_PRO.split('; ')
            add('uniprot:name', UniProtKB_ID, 'ensembl:gene_id', Ensembl[0])
            add('uniprot:name', UniProtKB_ID, 'ensembl:peptide_id', Ensembl_PRO[0])
            for e in Ensembl:
                add('ensembl:gene_id', e, 'uniprot:name', UniProtKB_ID)
            for e in Ensembl_PRO:
                add('ensembl:peptide_id', e, 'uniprot:name', UniProtKB_ID)
            seen_IDs.add(UniProtKB_ID)
        session.commit()
        loaded += 1
    return loaded

def _load_sec_ac(datadir, session):
    # This is a human readable file with a multi-line free text header
    # The start of data is indicated by
    # Secondary AC ... Primary AC
    # ____________     __________
    #
    # So, we skip until the first of these lines and then one more.

    loaded = 0
    data_next = False
    in_data = False
    for line in open(path.join(datadir, 'sec_ac.txt')):
        if in_data:
            sec,primary = line.strip().split()
            if session.query(Translation).filter(Translation.input_name == primary).limit(1).count():
                session.add(Translation(
                        'uniprot:accession', sec,
                        'uniprot:accession', primary))
                session.commit()
                loaded += 1
        elif data_next:
            in_data = True
        elif line.startswith('Secondary AC'):
            data_next = True
    return loaded

