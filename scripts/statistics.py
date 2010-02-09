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
import backend
from sqlalchemy import and_
import uniprot.models
import mgi.models
import esldb.models
import locatedb.models
from translations.services import translate
from collections import defaultdict

def esldbstats(session=None):
    if session is None: session = backend.create_session()

    # annotation type counts
    annot_uniprot = 0
    annot_similar = 0
    annot_experiment = 0
    annot_predict = 0

    # presence in uniprot
    specific_entry_only = 0
    entry_and_homolog = 0
    homolog_only = 0
    neither = 0

    # presence of ensembl ids in other databases
    ensembl_overlap_uniprot = 0
    ensembl_overlap_mgi = 0
    ensembl_overlap_locate = 0

    # species counts
    species = defaultdict(int)

    entries = session.query(esldb.models.Entry)
    for entry in entries:
        species[entry.species] += 1
        for annotation in entry.annotations:
            if annotation.type is 'experimental':
                annot_experiment += 1
            elif annotation.type is 'uniprot':
                annot_uniprot += 1
            elif annotation.type is 'similarity':
                annot_similar += 1
            elif annotation.type is 'predicted':
                annot_predict += 1

        if len(entry.uniprot_entries) > 0 and len(entry.uniprot_homologs) > 0:
            entry_and_homolog += 1
        elif len(entry.uniprot_entries) > 0:
            specific_entry_only += 1
        elif len(entry.uniprot_homologs) > 0:
            homolog_only += 1
        else:
            neither += 1 

    print 'Total eSLDB entries: %d' % entries.count()   
    for key in species.keys():
        print 'Total %s entries: %d' % (key, species[key])
    print 'Entries with locations found by:\n\tUniprot: %d\n\tExperiment: %d\n\tSimilarity: %d\n\tPrediction: %d' % (annot_uniprot, annot_experiment, annot_similar, annot_predict)
    print 'Entries with Uniprot verification:\n\tBy entry ID: %d\n\tBy homology: %d\n\tBy entry ID and homology: %d\n\tNeither: %d' % (specific_entry_only, homolog_only, entry_and_homolog, neither)

def uniprotstats(session=None):
    if session is None: session = backend.create_session()
    entries = session.query(uniprot.models.Entry)

    accessions = defaultdict(int)
    references = defaultdict(int)
    comments = defaultdict(int)

    for entry in entries:
        for accession in entry.accessions:
            accessions[accession] += 1

        for reference in entry.references:
            references[key] += 1

        for comment in entry.comments:
            comments[comment.type] += 1

        # what other statistics do we want from uniprot?

    print 'Total Uniprot entries: %d' % entries.count()
    print 'Unique accession #s: %d' % len(accessions)
    print 'Unique references: %d' % len(references)
    print 'Unique comment types: %d' % len(comments)

def locatestats(session=None):
    if session is None: session = backend.create_session()
    entries = session.query(locatedb.models.Entry)

    species = defaultdict(int)
    protein_sources = defaultdict(int)
    protein_accns = defaultdict(int)
    predictions = defaultdict(int)
    references = defaultdict(int)
    extrefs = defaultdict(int)
    extannots = defaultdict(int)

    for entry in entries:
        protein_sources[entry.source_name] += 1
        protein_accns[entry.accn] += 1

        for prediction in entry.predictions:
            predictions[prediction.method] += 1

        for reference in entry.references:
            references[reference.accn] += 1

        for annot in entry.annotations:
            extannots[annot.source_name] += 1

        for xref in entry.xrefs:
            extrefs[xref.source_name] += 1

    print 'Total LOCATE entries: %d' % entries.count()
    for organism in species.keys():
        print '\tTotal %s entries: %d' % (organism, species[organism])
    print 'Protein data sources: %d' % len(protein_sources)
    print 'Unique protein accession #s: %d' % len(protein_accns)
    print 'Unique SCL prediction methods: %d' % len(predictions)
    print 'Unique references cited: %d' % len(references)
    print 'Unique external annotations: %d' % len(extannots)
    print 'Unique external references: %d' % len(extrefs)

def mgistats(session=None):
    if session is None: session = backend.create_session()
    entries = session.query(mgi.models.Entry)

    # number of unique PubMed references
    pubmedids = defaultdict(int)
    evidence = defaultdict(int)

    for entry in entries:
        for annotation in entry.annotations:
            pubmedids[annotation.pubmedid] += 1 
            evidence[annotation.evidence] += 1

    print 'Total MGI entries: %d' % entries.count()
    print 'Unique PubMed references: %d' % len(pubmedids)
    print 'Unique Evidence identifiers: %d' % len(evidence)
