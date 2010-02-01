# -*- coding: utf-8 -*-
# Copyright (C) 2009, Shannon Quinn <squinn@cmu.edu>
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
from collections import defaultdict
from os import path
import models

_basedir = path.dirname(path.abspath(__file__))

inputfilename_human = path.abspath(path.join(_basedir, '../../databases/eSLDB_Homo_sapiens.txt'))
inputfilename_mouse = path.abspath(path.join(_basedir, '../../databases/eSLDB_Mus_musculus.txt'))

def load(filename, dbtype, create_session):
    '''
    load(filename, dbtype, create_session)

    Load an eSLDB database-download file into a local relational database

    Parameters
    ----------
      filename : The name of the eSLDB file
      dbtype : indicates the type of organism in the eSLDB file (mouse, human, etc)
      create_session : Callable object which returns an sqlalchemy session

    Returns
    -------
      num_entries : Number of entries loaded into the local database

    References
    ----------
    To download the database files:
    http://gpcr.biocomp.unibo.it/esldb/download.htm
    '''
    session = create_session()
    entries = set()

    # loop through the entries in the file
    for line in file(filename):
        line = line.strip()
        if line.startswith('eSLDB code'):
            continue

        # split the line on tabs
        eSLDB_code, \
        orig_db_code, \
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
            entries.add(eSLDB_code)
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

        # finally, add the uniprot data, if it exists
        if uniprot_entry != 'None':
            uniprot = models.UniprotEntry(eSLDB_code, uniprot_entry)
            session.add(uniprot)
        elif uniprot_homolog != 'None':
            uniprot = models.UniprotHomolog(eSLDB_code, uniprot_homolog)
            session.add(uniprot)

        # commit this session's additions
        session.commit()

    # all done! return the number of entries loaded
    return len(entries)
