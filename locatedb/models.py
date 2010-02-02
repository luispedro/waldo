# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
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
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base
from backend import Base

class Entry(Base):
    __tablename__ = 'locate_entries'
    locate_id = Column(Integer(11), primary_key=True)
    dbtype = Column(String(30), nullable=True)
    location_notes = Column(String(100), nullable=True)
    source_name = Column(String(50))
    source_id = Column(Integer(11))
    accn = Column(String(20))

    def __init__(self, id, source_name, source_id, accn, dbtype=None, location_notes=None):
        self.locate_id = id
        self.source_name = source_name
        self.source_id = source_id
        self.accn = accn
        self.dbtype = dbtype
        self.location_notes = location_notes 

class Isoform(Base):
    __tablename__ = 'locate_isoforms'
    isoform_id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.locate_id'))
    isoform_class = Column(String(20))
    isoform_name = Column(String(30))

    def __init__(self, locate_id, isoclass, isoname):
        self.locate_id = locate_id
        self.isoform_class = isoclass
        self.isoform_name = isoname

class Image(Base):
    __tablename__ = 'locate_images'
    image_id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.locate_id'))
    is_coloc = Column(Boolean)
    filename = Column(String(100))
    celltype = Column(String(50))
    magnification = Column(String(10))
    tag = Column(String(30))
    epitope = Column(String(30))
    channel = Column(String(20))
    coloc = Column(String(20), nullable=True)
    channel1 = Column(String(30), nullable=True)
    channel2 = Column(String(30), nullable=True)

    def __init__(self, locate_id, is_coloc, filename, celltype, magnification, tag, epitope, channel, coloc=None, channel1=None, channel2=None):
        self.locate_id = locate_id
        self.is_coloc = is_coloc
        self.filename = filename
        self.celltype = celltype
        self.magnification = magnification
        self.tag = tag
        self.epitope = epitope
        self.channel = channel
        self.coloc = coloc
        self.channel1 = channel1
        self.channel2 = channel2

class Predictions(Base):
    __tablename__ = 'locate_predictions'
    predict_id = Column(Integr(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.locate_id'))
    source_id = Column(Integer(11))
    method = Column(String(30))
    location = Column(String(50))
    goid = Column(String(50))
    evaluation = Column(Float)

    def __init__(self, locate_id, source_id, method, location, goid, evaluation):
        self.locate_id = locate_id
        self.source_id = source_id
        self.method = method
        self.location = location
        self.goid = goid
        self.evaluation = evaluation

class Literature(Base):
    __tablename__ = 'locate_literature'
    ref_id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.locate_id'))
    author = Column(String(200))
    title = Column(String(200))
    citation = Column(String(100))
    organism = Column(String(50))
    notes = Column(String(50), nullable=True)
    date_analyzed = Column(Date)
    source_id = Column(Integer(11))
    source_name = Column(String(50))
    accn = Column(String(20))

    def __init__(self, locate_id, author, title, citation, organism, date_analyzed, source_id, source_name, accn, notes=None):
        self.locate_id = locate_id
        self.author = author
        self.title = title
        self.citation = citation
        self.organism = organism
        self.notes = notes
        self.date_analyzed = date_analyzed
        self.source_id = source_id
        self.source_name = source_name
        self.accn = accn

class Annotation(Base):
    __tablename__ = 'locate_annotations'
    annot_id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.locate_id'))
    evidence = Column(String(50))
    source_id = Column(Integer(11))
    source_name = Column(String(50))
    accn = Column(String(20))

    def __init__(self, locate_id, evidence, source_id, source_name, accn):
        self.locate_id = locate_id
        self.evidence = evidence
        self.source_id = source_id
        self.source_name = source_name
        self.accn = accn

class Location(Base):
    __tablename__ = 'locate_locations'
    location_id = Column(Integer(11), primary_key=True)
    literature_id = Column(Integer(11), ForeignKey('locate_literature.ref_id'))
    externalannot_id = Column(Integer(11), ForeignKey('locate_annotationst.annot_id'))
    goid = Column(String(50))
    tier1 = Column(String(100))
    tier2 = Column(String(100), nullable=True)
    tier3 = Column(String(100), nullable=True)

    def __init__(self, lit_id, ext_id, goid, tier1, tier2=None, tier3=None):
        self.literature_id = lit_id
        self.externalannot_id = ext_id
        self.goid = goid
        self.tier1 = tier1
        self.tier2 = tier2
        self.tier3 = tier3

class ExternalDatabase(Base):
    __tablename__ = 'locate_externaldatabases'
    xref_id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.locate_id'))
    source_id = Column(Integer(11))
    source_name = Column(String(50))
    accn = Column(String(20))

    def __init__(self, locate_id, source_id, source_name, accn):
        self.locate_id = locate_id
        self.source_id = source_id
        self.source_name = source_name
        self.accn = accn
