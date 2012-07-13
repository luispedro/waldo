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

from __future__ import division
from sqlalchemy import Column, Boolean, String, Integer, ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base
from waldo.backend import Base

class Isoform(Base):
    __tablename__ = 'locate_isoforms'
    id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.id'), index=True)
    isoform_class = Column(String(20))
    isoform_name = Column(String(30))

    def __init__(self, isoclass, isoname):
        self.isoform_class = isoclass
        self.isoform_name = isoname

class Image(Base):
    __tablename__ = 'locate_images'
    id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.id'), index=True)
    filename = Column(String(50))
    is_coloc = Column(Boolean)
    celltype = Column(String(100))
    magnification = Column(String(30))
    tag = Column(String(100))
    epitope = Column(String(100))
    channel = Column(String(100))
    channel1 = Column(String(100), nullable=True)
    channel2 = Column(String(100), nullable=True)
    coloc = Column(String(100))

    def __init__(self, filename, is_coloc, celltype, magnification, tag, epitope, channel, channel1, channel2, coloc):
        self.filename = filename
        self.is_coloc = is_coloc
        self.celltype = celltype
        self.magnification = magnification
        self.tag = tag
        self.epitope = epitope
        self.channel = channel
        self.channel1 = channel1
        self.channel2 = channel2
        self.coloc = coloc


class LocatePrediction(Base):
    __tablename__ = 'locate_predictions'
    id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.id'), index=True)
    source_id = Column(Integer(11))
    method = Column(String(30))
    location = Column(String(50))
    go_id = Column(String(50))

    def __init__(self, source_id, method, location, go_id):
        self.source_id = source_id
        self.method = method
        self.location = location
        self.go_id = go_id

class Literature(Base):
    __tablename__ = 'locate_literature'
    id = Column(Integer, primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.id'), index=True)
    authors = Column(String(200))
    title = Column(String(200))
    citation = Column(String(100))
    source_id = Column(Integer(11))
    source_name = Column(String(50))
    accn = Column(String(20))


    def gen_citation(self):
        return '<cite>%s</cite> by <cite>%s</cite> (%s)' % (self.title, self.authors, self.citation)

    def gen_url(self):
        return None

    class LiteratureLocation(Base):
        __tablename__ = 'locate_literature_location'
        id = Column(Integer, primary_key=True)
        literature_id = Column(Integer, ForeignKey('locate_literature.id'), index=True)
        go_id = Column(String(16))

        def __init__(self, go_id):
            self.go_id = go_id

    locations = relation(LiteratureLocation)

    def __init__(self, authors, title, citation, source_id, source_name, accn, locations):
        self.authors = authors
        self.title = title
        self.citation = citation
        self.source_id = source_id
        self.source_name = source_name
        self.accn = accn
        self.locations = locations

class LocateAnnotation(Base):
    __tablename__ = 'locate_annotations'
    id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer, ForeignKey('locate_entries.id'), index=True)
    evidence = Column(String(64))
    source_id = Column(Integer(11))
    source_name = Column(String(50))
    accn = Column(String(20))
    go_id = Column(String(32))
    evidence_code = None


    def __init__(self, evidence, source_id, source_name, accn, go_id):
        self.evidence = evidence
        self.source_id = source_id
        self.source_name = source_name
        self.accn = accn
        self.go_id = go_id

class ExternalReference(Base):
    __tablename__ = 'locate_externalreferences'
    xref_id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.id'), index=True)
    source_id = Column(Integer(11))
    source_name = Column(String(50))
    accn = Column(String(20))

    def __init__(self, source_id, source_name, accn):
        self.source_id = source_id
        self.source_name = source_name
        self.accn = accn

class LocateEntry(Base):
    __tablename__ = 'locate_entries'
    id = Column(Integer(11), primary_key=True)
    organism = Column(String(30), nullable=True)
    name = Column(String(50))
    isoforms = relation(Isoform)
    predictions = relation(LocatePrediction)
    references = relation(Literature)
    go_annotations = relation(LocateAnnotation)
    xrefs = relation(ExternalReference)
    images = relation(Image)

    @property
    def internal_id(self):
        return self.id

    @property
    def organisms(self):
        return [self.organism]

    def __init__(self, id, name, isoforms, predictions, references, go_annotations, locations, images, xrefs, organism=None):
        self.id = id
        self.name = name
        self.organism = organism
        self.isoforms = isoforms
        self.predictions = predictions
        self.references = references
        self.go_annotations = go_annotations
        self.locations = locations
        self.images = images
        self.xrefs = xrefs

Entry = LocateEntry
Prediction = LocatePrediction
Annotation = LocateAnnotation

