# -*- coding: utf-8 -*-
# Copyright (C) 2009, Luís Pedro Coelho <lpc@cmu.edu>
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

from waldo.translations.models import Translation
import models

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))
def load(dirname=None, create_session=None):
    '''
    nr_loaded = load(dirname={data/}, create_session={backend.create_session})

    Loads gene_annotation.mgi and MRK_ENSEMBL.rpt files from MGI

    Parameters
    ----------
      dirname : base directory for data.

    Returns
    -------
      Nr of annotation entries loaded.

    References
    ----------

    For the file formats see:
    ftp://ftp.informatics.jax.org/pub/reports/index.html
    http://www.geneontology.org/GO.format.gaf-1_0.shtml
    http://wiki.geneontology.org/index.php/GAF_2.0
    '''
    if dirname is None: dirname = _datadir
    if create_session is None:
        import waldo.backend
        create_session = waldo.backend.create_session
    session = create_session()
    loaded = _load_gene_annotation(path.join(dirname, 'gene_association.mgi'), session)
    _load_mrk_ensembl(path.join(dirname, 'MRK_ENSEMBL.rpt'), session)
    return loaded

def _load_gene_annotation(filename, session):
    entries = set()
    loaded = 0
    for line in file(filename):
        if line[-1] == '\n': line = line[:-1]
        # DO NOT USE
        # line = line.strip()
        #
        # The reason is that there might be empty fields at the end
        # in which case, the line will end with '\t\t\n'. split()
        # handles this case correctly, but strip() would remove the extra
        # tabs.
        if line[0] == '!':
            if line.startswith('!gaf-version:'):
                if not line == '!gaf-version: 2.0':
                    raise IOError("waldo.go.load: Cannot parse. Wrong GAF version.\nHeader line: %s" % line)
            continue
        DB, \
         DB_object_id, \
         DB_object_symbol, \
         qualifier, \
         go_id, \
         db_ref, \
         evidence_code, \
         with_or_from, \
         aspect, \
         DB_object_name, \
         DB_object_synonym, \
         DB_object_type, \
         taxon, \
         date, \
         assigned_by, \
         annotation_cross_products, \
         gene_products = line.split('\t')

        if aspect == 'C':
            if DB_object_id not in entries:
                entry = models.Entry(DB_object_id, DB_object_name)
                entries.add(DB_object_id)
                session.add(entry)
                loaded += 1
            annotation = models.GOAnnotation(DB_object_id, go_id, assigned_by)
            session.add(annotation)
            if (loaded % 1024) == 0:
                session.commit()
    session.commit()
    return loaded

def _load_mrk_ensembl(filename, session):
    for i,line in enumerate(file(filename)):
        line = line.strip()
        mgi_accession, marker_sym, marker_name, cm_pos, chromosome, ensembl_id = line.split('\t')
        session.add_all([
                Translation('ensembl:gene_id', ensembl_id, 'mgi:id', mgi_accession),
                Translation('ensembl:gene_id', ensembl_id, 'mgi:symbol', marker_sym),
                Translation('ensembl:gene_id', ensembl_id, 'mgi:name', marker_name),
                ]
                )
        if (i % 1024) == 0:
            session.commit()
    session.commit()