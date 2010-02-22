# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from collections import defaultdict
from os import path
import models
from waldo.translations.models import Translation

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))

_mouse = 'eSLDB_Mus_musculus.txt'
_human = 'eSLDB_Homo_sapiens.txt'

def load(dirname=None, create_session=None):
    '''
    num_entries = load(dirname={data/}, create_session={backend.create_session})

    Load an eSLDB database-download file into a local relational database

    Parameters
    ----------
      dirname : Base directory containing the database files
      create_session : Callable object which returns an sqlalchemy session

    Returns
    -------
      num_entries : Number of entries loaded into the local database

    References
    ----------
    To download the database files:
    http://gpcr.biocomp.unibo.it/esldb/download.htm
    '''
    if dirname is None: dirname = _datadir
    if create_session is None:
        import waldo.backend
        create_session = waldo.backend.create_session
    session = create_session()

    # loop through the entries in the file
    count = _process_file(path.join(dirname, _mouse), 'mouse', session)
    count += _process_file(path.join(dirname, _human), 'human', session)
    return count

def _process_file(filename, dbtype, session):
    entries = defaultdict(str)
    count = 0
    for line in file(filename):
        count += 1
        line = line.strip()
        if line.startswith('eSLDB code') or len(line.split('\t')) < 10:
            continue

        # split the line on tabs
        eSLDB_code, \
        ensembl_peptide, \
        exp_annotation, \
        uniprot_annotation, \
        uniprot_entry, \
        sim_annotation, \
        uniprot_homolog, \
        e_value, \
        prediction, \
        aa_sequence, \
        common_name = line.split('\t')

        # create sqlalchemy objects and insert them
        if eSLDB_code not in entries:
            # create the entry itself
            entry = models.Entry(eSLDB_code, dbtype)
            entries[eSLDB_code] = []
            session.add(entry)

        # now all the annotations
        if exp_annotation != 'None':
            annotation = models.Annotation(eSLDB_code, 'experimental', exp_annotation)
            session.add(annotation)
        if uniprot_annotation != 'None':
            annotation = models.Annotation(eSLDB_code, 'uniprot', uniprot_annotation)
            session.add(annotation)
        if sim_annotation != 'None':
            annotation = models.Annotation(eSLDB_code, 'similarity', sim_annotation)
            session.add(annotation)
        if prediction != 'None':
            annotation = models.Annotation(eSLDB_code, 'predicted', prediction)
            session.add(annotation)

        # add the uniprot data, if it exists
        if uniprot_entry != 'None':
            uniprot = models.UniprotEntry(eSLDB_code, uniprot_entry)
            session.add(uniprot)
        elif uniprot_homolog != 'None':
            uniprot = models.UniprotHomolog(eSLDB_code, uniprot_homolog)
            session.add(uniprot)

        # provide the ensembl ID translations
        # PROBLEM: eSLDB, in its awful organizational format, will have multiple 
        # lines in the file with the same eSLDB_code AND ensembl peptide ID
        # hence we have to track each one as it occurs
        if ensembl_peptide not in entries[eSLDB_code]:
            session.add(Translation('ensembl:peptide_id', ensembl_peptide, 'esldb:id', eSLDB_code))
            session.add(Translation('esldb:id', eSLDB_code, 'ensembl:peptide_id', ensembl_peptide))
            entries[eSLDB_code].append(ensembl_peptide)

        # commit this session's additions
        session.commit()
    return len(entries)
