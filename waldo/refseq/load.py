# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012, Luis Pedro Coelho <luis@luispedro.org>
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
from os import path

import waldo.go
from waldo.translations.models import Translation
from waldo.tools import _gzip_open

_inputfilename = 'gene2ensembl.gz'

def clear(create_session=None):
    pass


def load(datadir, create_session=None, mouse_only=True):
    '''
    nr_loaded = load(datadir, create_session={backend.create_session}, mouse_only=True)

    Parameters
    ----------
    datadir : str
        Directory containing the gene2ensembl.gz file
    create_session : callable, optional
        a callable that returns an sqlalchemy session
    mouse_only : bool, optional
        whether to only load mouse data
        Currently, only ``mouse_only=True`` is implemented!

    Returns
    -------
    nr_loaded : int
        Nr. of entries loaded
    '''
    from waldo.backend import call_create_session
    filename = path.join(datadir, _inputfilename)
    session = call_create_session(create_session)
    input = _gzip_open(filename)
    header = input.readline()

    if not mouse_only:
        raise NotImplementedError('waldo.refseq.load: Cannot load non-mouse entries')

    nr_loaded = 0
    for line in input:
        tax_id, \
        gene_id, \
        ensembl_gene, \
        rna_accession, \
        emsembl_trans, \
        protein_accession, \
        ensembl_peptide = line.strip().split('\t')
        if ensembl_peptide.find('ENSMUSP') == -1:
            continue
        protein_accession, version = protein_accession.split('.')
        session.add(Translation(
                    'ensembl:peptide_id', ensembl_peptide,
                    'refseq:accession', protein_accession))
        session.add(Translation(
                    'refseq:accession', protein_accession,
                    'ensembl:peptide_id', ensembl_peptide))
        session.add(Translation(
                    'ensembl:gene_id', ensembl_gene,
                    'refseq:accession', protein_accession))
        session.add(Translation(
                    'refseq:accession', protein_accession,
                    'ensembl:gene_id', ensembl_gene))
        session.commit()
        nr_loaded += 1
    return nr_loaded

