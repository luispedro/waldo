# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# License: MIT

from __future__ import division
from waldo.nog import models
from os import path
import os

from waldo.tools import _gzip_open

_inputfilename = 'maNOG.mapping.txt.gz'

def _accept_species(sp, name):
    if sp == 'Mus Musculus': return name.startswith('ENSMUSP')
    if sp == 'Homo Sapiens': return name.startswith('ENSP0')
    raise ValueError('waldo.nog.load: I cannot recognise species `%s`' % sp)


def clear(create_session=None):
    '''
    clear()

    Removes all NOG related information
    '''
    from waldo.backend import call_create_session
    session = call_create_session(create_session)
    session.query(models.NogEntry).delete()
    session.commit()


def load(datadir, create_session=None, species=('Mus Musculus', 'Homo Sapiens')):
    '''
    nr_loaded = load(datadir, create_session={backend.create_session}, species=['Mus Musculus, Homo Sapiens')

    Load NOG entries file file into database

    Parameters
    ----------
    datadir : str
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
    from waldo.backend import call_create_session
    session = call_create_session(create_session)
    if datadir is None: datadir = _datadir
    nr_loaded = 0
    filename = path.join(datadir, _inputfilename)
    inputfile = _gzip_open(filename)
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

