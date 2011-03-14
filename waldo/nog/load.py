# -*- coding: utf-8 -*-
# Copyright (C) 2011, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# License: MIT

from __future__ import division
from waldo.nog import models
from os import path
import os
import gzip

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))
_inputfilename = 'maNOG.mapping.txt.gz'

def _accept_species(sp, name):
    if sp == 'Mus Musculus': return name.startswith('ENSMUSP')
    if sp == 'Homo Sapiens': return name.startswith('ENSP0')
    raise ValueError('waldo.nog.load: I cannot recognise species `%s`' % sp)

def load(dirname=None, create_session=None, species=('Mus Musculus', 'Homo Sapiens')):
    '''
    nr_loaded = load(dirname={data/}, create_session={backend.create_session}, species=['Mus Musculus, Homo Sapiens')

    Load NOG entries file file into database

    Parameters
    ----------
    dirname : str, optional
        Directory containing the maNOG.mapping.txt.gz file
    create_session : callable, optional
        a callable object that returns an sqlalchemy session
    species : sequence
        species to load

    Returns
    -------
    nr_loaded : integer
        Nr. of entries loaded
    '''
    if dirname is None: dirname = _datadir
    if create_session is None:
        from waldo import backend
        create_session = backend.create_session
    session = create_session()
    nr_loaded = 0
    filename = path.join(dirname,_inputfilename)
    inputfile = gzip.GzipFile(filename)
    header = inputfile.readline()
    for line in inputfile:
        prot_name, \
            start, \
            end, \
            group, \
            description = line.strip().split('\t')
        _, prot_name = prot_name.split('.')
        group = group[len('maNOG'):]
        group = int(group)
        for sp in species:
            if _accept_species(sp, prot_name):
                entry = models.NogEntry(prot_name, group)
                session.add(entry)
                session.commit()
                nr_loaded += 1
                break
    return nr_loaded

