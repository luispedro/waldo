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
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relation, backref
from waldo.backend import Base

class Accession(Base):
    __tablename__ = 'uniprot_accession'
    
    # We cannot use accession as primary key because they are not unique.
    # Sometimes, one single accession number has been demerged into multiple entries.
    acc_name_id = Column(Integer, primary_key=True)
    uniprot_name = Column(String(32), ForeignKey('uniprot_entry.name'), index=True)
    accession = Column(String(8), nullable=False)

    def __init__(self, accession):
        self.accession = accession

class GoAnnotation(Base):
    __tablename__ = 'uniprot_go_annotation'
    go_ann_id = Column(Integer, primary_key=True)
    uniprot_name = Column(String(32), ForeignKey('uniprot_entry.name'), index=True)
    go_id = Column(String(32))
    evidence_code = Column(String(32))

    def __init__(self, go_id, evidence_code):
        self.go_id = go_id
        self.evidence_code = evidence_code

    def __str__(self):
        return 'GoAnnotation({0})'.format(self.go_id)

    def __repr__(self):
        return 'GoAnnotation({0}, {1}, {2}, {3})'.format(self.go_ann_id, self.uniprot_name, self.go_id, self.evidence_code)

class Reference(Base):
    __tablename__ = 'uniprot_reference'
    refid = Column(Integer, primary_key=True)
    uniprot_name = Column(String(32), ForeignKey('uniprot_entry.name'), index=True)
    key = Column(String(64))
    type = Column(String(32))
    title = Column(String(512))
    authors = Column(String(512))
    dbRef = Column(String(64))

    def gen_citation(self):
        return '<a href="%s"><cite>%s</cite></a> by <cite>%s</cite>' % (self.gen_url(), self.title, self.authors)

    def gen_url(self):
        rtype,_,code = self.dbRef.partition(':')
        if rtype == "DOI":
            return 'http://dx.doi.org/%s' % code
        return 'http://www.ncbi.nlm.nih.gov/pubmed/%s' % code

    def __init__(self, key, type, title, authors, dbRef):
        self.type = type
        self.key = key
        self.title = title
        self.authors = authors
        self.dbRef = dbRef

class Comment(Base):
    __tablename__ = 'uniprot_comment'
    commentid = Column(Integer, primary_key=True)
    uniprot_name = Column(String(32), ForeignKey('uniprot_entry.name'), index=True)
    type = Column(String(64))
    text = Column(String(512))

    def __init__(self, type, text):
        self.type = type
        self.text = text

class Organism(Base):
    __tablename__ = 'uniprot_organism_entry'
    oid = Column(Integer, primary_key=True)
    uniprot_name = Column(String(32), ForeignKey('uniprot_entry.name'), index=True)
    organism = Column(String(64))

    def __init__(self, organism):
        self.organism = organism

    def __str__(self):
        return str(self.organism)

    def __unicode__(self):
        return unicode(self.organism, 'utf-8')

class UniprotEntry(Base):
    __tablename__ = 'uniprot_entry'
    name = Column(String(32), nullable=False, primary_key=True)
    rname = Column(String(128), nullable=False)
    gname = Column(String(128), nullable=True)
    accessions = relation(Accession)
    references = relation(Reference)
    comments = relation(Comment)
    go_annotations = relation(GoAnnotation)
    sequence = Column(Text)
    organisms = relation(Organism)


    @property
    def internal_id(self):
        return self.name

    def __init__(self, name, rname, gname, accessions, comments, references, go_annotations, sequence, organisms):
        self.name = name
        self.rname = rname
        self.gname = gname
        if type(accessions[0]) in (str, unicode):
            accessions = map(Accession, accessions)
        if organisms and type(organisms[0]) in (str, unicode):
            organisms = map(Organism, organisms)

        self.accessions = accessions
        self.references = references
        self.comments = comments
        self.go_annotations = go_annotations
        self.sequence = sequence
        self.organisms = organisms

    def __repr__(self):
        return '<Uniprot Entry: %s>' % self.name

Entry = UniprotEntry
