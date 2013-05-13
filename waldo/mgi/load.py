# -*- coding: utf-8 -*-
# Copyright (C) 2009-2013, Luis Pedro Coelho <luis@luispedro.org>
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


def clear(create_session=None):
    '''
    clear()

    Removes all MGI related information
    '''
    from waldo.backend import call_create_session
    session = call_create_session(create_session)
    session.query(models.GOAnnotation).delete()
    session.query(models.MGIEntry).delete()
    session.commit()


def load(datadir, create_session=None):
    '''
    nr_loaded = load(datadir, create_session={backend.create_session})

    Loads gene_annotation.mgi and MRK_ENSEMBL.rpt files from MGI

    Parameters
    ----------
      datadir : str
        base directory for data.

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
    from waldo.backend import call_create_session
    if datadir is None: datadir = _datadir
    session = call_create_session(create_session)
    loaded = _load_gene_annotation(path.join(datadir, 'gene_association.mgi'), session)
    _load_mrk_ensembl(path.join(datadir, 'MRK_ENSEMBL.rpt'), session)
    _load_pubmed_ids(path.join(datadir, 'MRK_Reference.rpt'), session)
    return loaded

def _load_gene_annotation(filename, session):
    entries = set()
    loaded = 0
    for line in open(filename):
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
                    raise IOError("waldo.mgi.load: Cannot parse. Wrong GAF version.\nHeader line: %s" % line)
            continue
        
        try:
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
        except ValueError:
            pass
            # don't really need to worry about this

        if aspect == 'C':
            if DB_object_id not in entries:
                entry = models.Entry(DB_object_id, DB_object_name)
                entries.add(DB_object_id)
                session.add(entry)
                loaded += 1
            annotation = models.GOAnnotation(DB_object_id, go_id, evidence_code, assigned_by)
            session.add(annotation)
            if len(session.new) > 512:
                session.commit()
    session.commit()
    return loaded

def _load_mrk_ensembl(filename, session):
    for line in open(filename):
        tokens = line.strip().split('\t')
        mgi_accession, marker_sym, marker_name, cm_pos, chromosome, ensembl_gene_id = tokens[:6]
        def add_synonym(namespace, name):
            session.add_all([
                    Translation(namespace, name, 'mgi:id', mgi_accession),
                    Translation(namespace, name, 'mgi:symbol', marker_sym),
                    Translation(namespace, name, 'mgi:name', marker_name),
                    Translation('mgi:id', mgi_accession, namespace, name),
                    Translation('mgi:symbol', marker_sym, namespace, name),
                    Translation('mgi:name', marker_name, namespace, name),
                    ])
        if len(tokens) > 6:
            transcript_ids = tokens[6]
            for id in transcript_ids.split():
                add_synonym('ensembl:transcript_id', id)
        if len(tokens) > 7:
            peptide_ids = tokens[7]
            for id in peptide_ids.split():
                add_synonym('ensembl:peptide_id', id)
        add_synonym('ensembl:gene_id', ensembl_gene_id)
        if len(session.new) > 512:
            session.commit()
    session.commit()

def _load_pubmed_ids(filename, session):
    '''
    For each line in the file, determine if the referenced MGI ID exists in database.
    If so, insert the associated PubMed IDs into SQLite.
    '''
    for line in open(filename):
        mgi_id, \
        mrk_symbol, \
        mrk_name, \
        mrk_synonym, \
        pubmed_ids = line.split('\t')

        # first, does mgi_id exist in our database?
        obj = session.query(models.Entry).filter(models.Entry.mgi_id == mgi_id).first()
        if obj is not None:

            # update the record to include the PubMed IDs
            obj.pubmedids = pubmed_ids
            if len(session.dirty) > 512:
                session.commit()
    session.commit()

