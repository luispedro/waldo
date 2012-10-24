# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import waldo.backend
from sqlalchemy import and_
from waldo.uniprot.models import Entry
from waldo.translations.services import translate
import urllib

_translate = {
        'EXP' : 'Inferred from Experiment',
        'IDA' : 'Inferred from Direct Assay',
        'IPI' : 'Inferred from Physical Interation',
        'IMP' : 'Inferred from Mutant Phenotype',
        'IGI' : 'Inferred from Genetic Interaction',
        'IEP' : 'Inferred from Expression Pattern',
        'ISS' : 'Inferred from Sequence or Structural Similarity',
        'ISA' : 'Inferred from Sequence Alignment',
        'ISO' : 'Inferred from Sequence Orthology',
        'ISM' : 'Inferred from Sequence Model',
        'IGC' : 'Inferred from Genomic Context',
        'RCA' : 'Inferred from Reviewed Computational Analysis',
        'TAS' : 'Traceable Author Statement',
        'NAS' : 'Non-traceable Author Statement',
        'IC'  : 'Inferred by Curator',
        'ND'  : 'No biological Data available',
        'IEA' : 'Inferred from Electronic Annotation',
        'NR'  : 'Not Recorded'
}

def from_ensembl_gene_id(ensembl_gene_id, session=None):
    '''
    name = from_ensembl_gene_id(ensembl_gene_id, session={backend.create_session()})

    Convert ensembl_gene_id to uniprot name (uniprot ID).

    Parameters
    ----------
    ensembl_gene_id : str
        Ensembl gene ID
    session : SQLAlchemy session
        Session to use (default: call backend.create_session())

    Returns
    -------
    name : str
        uniprot gene name
    '''
    return translate(ensembl_gene_id, 'ensembl:gene_id', 'uniprot:name', session)

def from_ensembl_peptide_id(ensembl_peptide_id, session=None):
    '''
    name = from ensembl_peptide_id(ensembl_peptide_id, session={backend.create_session()})

    Convert ensembl_peptide_id to Uniprot name/ID.

    Parameters
    ----------
    ensembl_peptide_id : str
        Ensembl protein ID
    session : SQLAlchemy session
        Session to use (default: create a new one)

    Returns
    -------
    name : str
        Uniprot peptide name
    '''
    return translate(ensembl_peptide_id, 'ensembl:peptide_id', 'uniprot:name', session)

def retrieve_go_annotations(name, session=None, return_evidence=False, only_cellular_component=True):
    '''
    go_ids = retrieve_go_annotations(name, session={backend.create_session()}, return_evidence=False, only_cellular_component=True)

    Retrieve GO ids by uniprot name.

    Parameters
    ----------
    name : str
        uniprot name
    session : SQLAlchemy session object, optional
        session to use (default: call backend.create_session())
    return_evidence : boolean, optional
        Whether to return evidence (default: False)
    only_cellular_component : boolean, optional
        Whether to return only GO terms in the cellular component space (default: True)

    Returns
    -------
    go_ids : list of str or list of (str,str)
        go terms (of the form "GO:00..."). If ``return_evidence``, then pairs
        are returned, where the second element is the evidence code.
    '''
    import waldo.go
    if session is None: session = waldo.backend.create_session()
    entr = session.query(Entry).filter(Entry.name == name).first()
    if entr is None:
        return []
    annotations = entr.go_annotations
    if only_cellular_component:
        def is_cellular_component(g):
            return waldo.go.is_cellular_component(g.go_id, session)
        annotations = filter(is_cellular_component, annotations)
    if return_evidence:
        return [(go.go_id, go.evidence_code) for go in annotations]
    return [go.go_id for go in annotations]

def retrieve_name_matches(term, session=None):
    '''
    entries = retrieve_name_matches(term, session={backend.create_session()})

    Retrieve Uniprot entries that match the given term, using full text search
    on the human readable protein names.

    Parameters
    ----------
    term : str
        A human readable protein name (or part of a name)
    session : SQLAlchemy session, optional
        SQLAlchemy session to use (default: create a new one)

    Returns
    -------
    entries : list of waldo.uniprot.model.Entry
        Objects whose readable names match
    '''
    if session is None: session = waldo.backend.create_session()
    return session.query(Entry).from_statement('select * from uniprot_entry where rname match "*' + term + '*"').all()

def retrieve_entry(id, session=None):
    '''
    entry = retrieve_entry(id, session={backend.create_session()})

    Retrieve Uniprot entry based on its identifier.

    Parameters
    ----------
    id : str
        Uniprot-specific identifier (i.e., Uniprot Name)
    session: SQLAlchemy session
        Session to use to use (default: create a new one)

    Returns
    -------
    entry : waldo.uniprot.models.Entry
    '''
    if session is None: session = waldo.backend.create_session()
    return session.query(Entry).filter(Entry.name == id).first()

def gen_url(id):
    '''
    url = gen_url(id)

    Generate URL for uniprot id `id`

    Parameters
    ----------
    id : str
        uniprot name or accession id

    Returns
    -------
    url : str
        web url of corresponding data page.
    '''
    return 'http://www.uniprot.org/uniprot/' + id

def translate_evidence_code(code):
    '''
    desc = translate_evidence_code(code)

    Translate an evidence and its source into a more readable description

    Parameters
    ----------
    code : str
        "evidence code:source" parsed from Uniprot database.

    Returns
    -------
    desc : str
        phrase describing the evidence code and its source.
    '''
    vals = code.split(':')
    return _translate.get(vals[0], 'Evidence code Unknown') + ' from ' + vals[1]

def retrieve_pubmed_abstract(pmid):
    '''
    abstract = retrieve_pubmed_abstract(pmid)

    Retrieves the abstract for a paper given by the PubMed id `pmid`

    Parameters
    ----------
    pmid : str
        A Pubmed id

    Returns
    -------
    abstract : str
        The abstract associated with the PubMed id's paper
    '''
    page = urllib.urlopen("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?id=%s&db=pubmed&rettype=abstract" % pmid)
    abstract = page.read()
    return abstract.partition('<pre>')[2].partition('</pre>')[0].rstrip()

def retrieve_doi_abstract(doi):
    '''
    abstract = retrieve_doi_abstract(doi)

    Retrieves the abstract for a paper given by the DOI id doi by looking up its Pubmed id

    This function queries the Entrez database online.

    Parameters
    ----------
    doi : str
        a DOI code

    Returns
    -------
    abstract : str
        The abstract associated with the DOI codes's paper, or None if no matching Pubmed id is found.
    '''
    from lxml import etree
    page = urllib.urlopen("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%s[aid]" % doi)
    xml = page.read()
    root = etree.fromstring(xml)
    if(root.find('Count').text == '0'):
        return None
    pmid = root.find('IdList').iterchildren().next().text
    return retrieve_pubmed_abstract(pmid)

