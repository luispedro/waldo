# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
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
      ensembl_gene_id : Ensembl gene ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      name : uniprot gene name
    '''
    return translate(ensembl_gene_id, 'ensembl:gene_id', 'uniprot:name', session)

def from_ensembl_peptide_id(ensembl_peptide_id, session=None):
    '''
    name = from ensembl_peptide_id(ensembl_peptide_id, session={backend.create_session()})

    Convert ensembl_peptide_id to Uniprot name/ID.

    Parameters
    ----------
      ensembl_peptide_id : Ensembl protein ID
      session : SQLAlchemy session to use (default: create a new one)

    Returns
    -------
      name : Uniprot peptide name
    '''
    return translate(ensembl_peptide_id, 'ensembl:peptide_id', 'uniprot:name', session)

def retrieve_go_annotations(name, session=None):
    '''
    go_ids = retrieve_go_annotations(name, session={backend.create_session()})

    Retrieve GO ids by uniprot name.

    Parameters
    ----------
    name : str
        uniprot name
    session : SQLAlchemy session object, optional
        session to use (default: call backend.create_session())

    Returns
    -------
    go_ids : list of str
        go terms (of the form "GO:00...")
    '''
    if session is None: session = waldo.backend.create_session()
    entr = session.query(Entry).filter(Entry.name == name).first()
    return [go.go_id for go in entr.go_annotations]

def retrieve_entry(id, session=None):
    '''
    entry = retrieve_entry(id, session={backend.create_session()})

    Retrieve Uniprot entry based on its identifier.

    Parameters
    ----------
      id : Uniprot-specific identifier
      session: SQLAlchemy session to use (default: create a new one)

    Returns
    -------
      entry : models.Entry object
    '''
    if session is None: session = waldo.backend.create_session()
    return session.query(Entry).filter(Entry.name == id).first()

def gen_url(id):
    '''
    url = gen_url(id)

    Generate URL for uniprot id `id`

    Parameters
    ----------
      id : uniprot name or accession id
    Returns
    -------
      url : web url of corresponding data page.
    '''
    return 'http://www.uniprot.org/uniprot/' + id

def translate_evidence_code(code):
    '''
    desc = translate_evidence_code(code)

    Translate an evidence and its source into a more readable description

    Parameters
    ----------
      code : "evidence code:source" parsed from Uniprot database.

    Returns
    -------
      desc : sentence describing the evidence code and its source.

    '''
    vals = code.split(':')
    return _translate.get(vals[0], 'Evidence code Unknown') + ' from ' + vals[1]

def retrieve_pubmed_abstract(pmid):
    '''
    abstract = retrieve_pubmed_abstract(pmid

    Retrieves the abstract for a paper given by the PubMed id pmid

    Parameters
    ----------
      pmid : a pubmed id

    Returns
    -------
      abstract : the abstract associated with the PubMed id's paper
    '''
    page = urllib.urlopen("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?id=%s&db=pubmed&rettype=abstract" % pmid)
    abstract = page.read()
    return abstract.partition('<pre>')[2].partition('</pre>')[0]
