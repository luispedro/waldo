# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012, Shannon Quinn <squinn@cmu.edu> and Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from os import path
import csv
import models
from waldo.translations.models import Translation

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))

_annot = 'subcellular_location.csv.zip'

def clear(create_session=None):
    '''
    clear()

    Removes all HPA related information
    '''
    session = call_create_sesssion(create_session)
    session.delete(models.Location)
    session.delete(models.HPAEntry)
    session.commit()


def load(dirname=None, create_session=None):
    '''
    num_entries = load(dirname={data/}, create_session={backend.create_session})

    Load the data from a subcellular location annotations file into the local 
    relational database

    Parameters
    ----------
    dirname : str, optional
        Base directory containing the annotations file (default: 'data/')
    create_session : callable, optional
        Callable object which returns an sqlalchemy session (default:
        waldo.backend.create_session)

    Returns
    -------
    num_entries : integer
        Number of entries loaded into the local database

    References
    ----------
      (none)

    '''
    import zipfile
    if dirname is None: dirname = _datadir
    if create_session is None:
        import waldo.backend
        create_session = waldo.backend.create_session
    session = create_session()
    zf = zipfile.ZipFile(path.join(dirname, _annot))
    inputf = zf.open(zf.filelist[0])


    # loop through the entries in the file
    csvreader = csv.reader(inputf, delimiter=',', quotechar='"')
    count = 0
    loc_names = []
    for row in csvreader:
        count += 1
        if count == 1:
            continue

        # loop through the list of comma-separated elements on this row
        gene, main_loc, other_loc, exp_type, rel = row

        locations = main_loc.split(";")
        if(other_loc != ""): 
            locations += other_loc.split(";")
    
        for name in locations:
            session.add(models.Location(name, gene))

        session.add(models.Entry(gene))

        session.commit()
        
    return count - 1 # since the first row wasn't an entry



