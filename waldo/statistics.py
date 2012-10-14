# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012, Shannon Quinn <squinn@cmu.edu> and Luis Pedro Coelho <luis@luispedro.org>
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

from __future__ import print_function

from collections import defaultdict
from sqlalchemy import and_, func
import waldo.backend
import waldo.uniprot.models
import waldo.mgi.models
import waldo.locate.models
from waldo.translations.services import translate

def uniprotstats(session=None):
    from waldo.uniprot.models import Entry, Reference, Accession, Comment
    if session is None:
        session = waldo.backend.create_session()
    print('Total Uniprot entries: {0}'.format(session.query(Entry).count()))
    print('Unique accession numbers: {0}'.format(session.query(Accession.accession).distinct().count()))
    print('Unique references: {0}'.format(session.query(Reference.key).distinct().count()))
    print('Unique comment types: {0}'.format(session.query(Comment.type).distinct().count()))


def locatestats(session=None):
    from waldo.locate.models import Entry, ExternalReference, Annotation, Literature, Location, Isoform, Image, Prediction
    if session is None: session = waldo.backend.create_session()
    q = session.query
    print('Total LOCATE entries: {0}'.format(q(Entry).count()))
    for organism,count in q(Entry.organism, func.count(Entry.organism)).group_by(Entry.organism):
        print('\tTotal {0} entries: {1}'.format(organism,count))
    print()
    print('Protein data sources: {0}'.format(q(Entry.source_name).distinct().count()))
    print('Unique protein accession numbers: {0}'.format(q(Entry.accn).distinct().count()))
    print('Unique SCL prediction methods: {0}'.format(q(Prediction.method).distinct().count()))
    print('Unique references cited: {0}'.format(q(Literature.accn).distinct().count()))
    print('Unique external annotations: {0}'.format(q(Annotation.id).distinct().count()))
    print('Unique external references: {0}'.format(q(ExternalReference.source_name).distinct().count()))

def mgistats(session=None):
    from waldo.uniprot.models import Entry, GOAnnotation
    if session is None:
        session = waldo.backend.create_session()
    entries = session.query(Entry)
    print('Total MGI entries: {0}'.format(entries.count()))
    print('Unique PubMed references: {0}'.format(session.query(Entry.pubmedids).distinct().count()))
    print('Unique Evidence identifiers: {0}'.format(session.query(GOAnnotation.evidence).distinct().count()))

