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
from sqlalchemy import and_, func
import waldo.backend
import waldo.uniprot.models
import waldo.mgi.models
import waldo.locate.models
from waldo.translations.services import translate

def uniprotstats(session=None):
    if session is None: session = waldo.backend.create_session()
    entries = session.query(waldo.uniprot.models.Entry)

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
    if session is None: session = waldo.backend.create_session()
    entries = session.query(waldo.locate.models.Entry)

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
    if session is None: session = waldo.backend.create_session()
    entries = session.query(waldo.mgi.models.Entry)

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
