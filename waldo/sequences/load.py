# -*- coding: utf-8 -*-
# Copyright (C) 2011, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# License: MIT

from __future__ import division
from waldo.sequences import fasta
from waldo.sequences import models
from os import path

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))
_inputfilename = 'Mus_musculus.NCBIM37.60.pep.all.fa.gz'

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
    filename = path.join(dirname, _inputfilename)
    if create_session is None:
        from waldo import backend
        create_session = backend.create_session
    session = create_session()
    nr_loaded = 0
    for seq in fasta.read(filename):
        peptide = seq.header.split()[0]
        aaseq = seq.sequence
        seq = models.EnsemblSequence(peptide, aaseq)
        session.add(seq)
        session.commit()
        nr_loaded += 1
    return nr_loaded

