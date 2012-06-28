# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# License: MIT

from __future__ import division
from waldo.sequences import fasta
from waldo.sequences import models
from waldo.translations.models import Translation
from os import path
import os
import glob

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))


def clear(create_session=None):
    '''
    clear()

    Removes all Sequence related information
    '''
    session = call_create_sesssion(create_session)
    session.delete(models.EnsemblSequence)
    session.commit()
def load(dirname=None, create_session=None):
    '''
    nr_loaded = load(dirname={data/}, create_session={backend.create_session})

    Load ENSEMBL FASTA file into database

    Parameters
    ----------
    dirname : str, optional
        Directory containing the FASTA file
    create_session : callable, optional
        a callable object that returns an sqlalchemy session

    Returns
    -------
    nr_loaded : integer
        Nr. of entries loaded
    '''
    if dirname is None: dirname = _datadir
    inputfilename = glob.glob(path.join(dirname,'Mus_musculus.NCBIM37.*.pep.all.fa.gz'))[0]
    filename = path.join(inputfilename)
    if create_session is None:
        from waldo import backend
        create_session = backend.create_session
    session = create_session()
    nr_loaded = 0
    for seq in fasta.read(filename):
        htokens = seq.header.split()
        peptide = htokens[0]
        gene = htokens[3]
        assert gene.startswith('gene:'), 'waldo.sequences.load'
        gene = gene[len('gene:'):]
        session.add(
            Translation(
                'ensembl:gene_id',
                gene,
                'ensembl:peptide_id',
                peptide))
        aaseq = seq.sequence
        seq = models.EnsemblSequence(peptide, aaseq)
        session.add(seq)
        session.commit()
        nr_loaded += 1
    return nr_loaded

