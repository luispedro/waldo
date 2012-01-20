# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import waldo.backend
from waldo.mgi.models import Entry
from waldo.translations.services import translate

def from_ensembl_gene_id(ensembl_gene_id, session=None):
    '''
    mgi_id = from_ensembl_gene_id(ensembl_gene_id, session={backend.create_session()})

    Convert ensembl_gene_id to mgi ID (MGI:00xxxxxx)

    Parameters
    ----------
      ensembl_gene_id : Ensembl gene ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      mgi_id : MGI ID
    '''
    return translate(ensembl_gene_id, 'ensembl:gene_id', 'mgi:id', session)

def from_ensembl_peptide_id(ensembl_peptide_id, session=None):
    '''
    mgi_id = from_ensembl_peptide_id(ensembl_peptide_id, session={backend.create_session()})

    Convert ensembl_peptide_id to mgi ID (MGI:00xxxxxx)

    Parameters
    ----------
      ensembl_peptide_id : Ensembl peptide ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      mgi_id : MGI ID
    '''
    return translate(ensembl_peptide_id, 'ensembl:peptide_id', 'mgi:id', session)

def retrieve_go_annotations(mgi_id, session=None):
    '''
    go_ids = retrieve_go_annotations(mgi_id, session={backend.create_session()})

    Retrieve GO ids by MGI ID.

    Parameters
    ----------
      mgi_id : mgi_id
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      go_ids : list of go terms (of the form "GO:00...")
    '''
    if session is None: session = waldo.backend.create_session()
    entr = session.query(Entry).filter(Entry.mgi_id == mgi_id).first()
    if entr is None:
        raise KeyError('waldo.mgi.retrieve_go_annotations: No entry for `%s`' % mgi_id)
    return [go.go_id for go in entr.go_annotations]

def retrieve_entry(id, session=None):
    '''
    entry = retrieve_entry(id, session={backend.create_session()})

    Retrieve MGI Entry object by its MGI ID.

    Parameters
    ----------
      id : MGI ID
      session: SQLAlchemy session to use (default: create a new one)

    Returns
    -------
      entry : models.Entry object
    '''
    if session is None: session = waldo.backend.create_session()
    return session.query(Entry).filter(Entry.mgi_id == id).first()


def gen_url(id):
    '''
    url = gen_url(id)

    Generate URL for MGI id `id`

    Parameters
    ----------
      id : MGI id
    Returns
    -------
      url : web url of corresponding data page.
    '''
    return 'http://www.informatics.jax.org/searchtool/Search.do?query=' + id

