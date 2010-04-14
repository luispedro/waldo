# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from os import path
import csv
import models
from waldo.translations.models import Translation

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))

_annot = 'hpa_annotations.csv'

def load(dirname=None, create_session=None):
    '''
    num_entries = load(dirname={data/}, create_session={backend.create_session})

    Load the data from an HPA annotations file into the local relational database

    Parameters
    ----------
      dirname : Base directory containing the annotations file
      create_session : Callable object which returns an sqlalchemy session

    Returns
    -------
      num_entries : Number of entries loaded into the local database

    References
    ----------
      (none)

    '''
    if dirname is None: dirname = _datadir
    if create_session is None:
        import waldo.backend
        create_session = waldo.backend.create_session
    session = create_session()

    # loop through the entries in the file
    csvreader = csv.reader(open(path.join(dirname, _annot)), delimiter=',', quotechar='"')
    count = 0
    loc_names = []
    for row in csvreader:
        count += 1
        if count == 1:
            loc_names = [n.replace('"','') for n in row[9:24]]
            continue

        # loop through the list of comma-separated elements on this row
        antibody, \
        plate_id, \
        well, \
        cell_line, \
        ensembl_gene, \
        if_annot_summary, \
        if_annot_id, \
        if_stain_intensity_id, \
        unspecific, \
        loc_nucleus, \
        loc_cytoplasm, \
        loc_plasma_membrane, \
        loc_nuclear_membrane, \
        loc_nucleoli, \
        loc_mitochondria, \
        loc_er, \
        loc_golgi, \
        loc_lys_pero_endo, \
        loc_cytoskeleton, \
        loc_ecm, \
        loc_nucleus_without_nucleoli, \
        loc_centrosome, \
        loc_cell_junctions, \
        loc_focal_adhesions, \
        stain_granular, \
        stain_smooth, \
        stain_cluster, \
        stain_fibrous, \
        stain_spotty, \
        stain_speckle, \
        stain_aggregate, \
        if_reliability_score_id = row

        locations = row[9:24]
        for loc_flag,name in zip(locations, loc_names):
            if loc_flag == "1":
                session.add(models.Location(name, antibody))

        session.add(models.Entry(antibody, ensembl_gene, cell_line))
        session.add(Translation('ensembl:gene_id', ensembl_gene, 'hpa:id', antibody))
        session.add(Translation('hpa:id', antibody, 'ensembl:gene_id', ensembl_gene))
        session.commit()
        
    return count - 1 # since the first row wasn't an entry

