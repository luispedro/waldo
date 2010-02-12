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
from waldo.backend import Base

class Isoform(Base):
    __tablename__ = 'locate_isoforms'
    isoform_id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.locate_id'))
    isoform_class = Column(String(20))
    isoform_name = Column(String(30))

    def __init__(self, isoclass, isoname):
        self.isoform_class = isoclass
        self.isoform_name = isoname

class Prediction(Base):
    __tablename__ = 'locate_predictions'
    predict_id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.locate_id'))
    source_id = Column(Integer(11))
    method = Column(String(30))
    location = Column(String(50))
    goid = Column(String(50))

    def __init__(self, source_id, method, location, goid):
        self.source_id = source_id
        self.method = method
        self.location = location
        self.goid = goid

class Location(Base):
    __tablename__ = 'locate_locations'
    location_id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.locate_id'), nullable=True)
    literature_id = Column(Integer(11), ForeignKey('locate_literature.ref_id'), nullable=True)
    externalannot_id = Column(Integer(11), ForeignKey('locate_annotations.annot_id'), nullable=True)
    goid = Column(String(50))
    tier1 = Column(String(100), nullable=True)
    tier2 = Column(String(100), nullable=True)
    tier3 = Column(String(100), nullable=True)

    def __init__(self, goid, tier1, tier2=None, tier3=None):
        self.goid = goid
        self.tier1 = tier1
        self.tier2 = tier2
        self.tier3 = tier3

        # this section is a dirty hack to get around getattr() and the possible
        # (and unwanted) conversion of None to 'None'...this should be fixed
        # from within load.py FIXME
        if tier1 is not None: self.tier1 = unicode(tier1)
        if tier2 is not None: self.tier2 = unicode(tier2)
        if tier3 is not None: self.tier3 = unicode(tier3)

class Literature(Base):
    __tablename__ = 'locate_literature'
    ref_id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.locate_id'))
    author = Column(String(200))
    title = Column(String(200))
    citation = Column(String(100))
    source_id = Column(Integer(11))
    source_name = Column(String(50))
    accn = Column(String(20))
    locations = relation(Location)

    def __init__(self, author, title, citation, source_id, source_name, accn, locations):
        self.author = author
        self.title = title
        self.citation = citation
        self.source_id = source_id
        self.source_name = source_name
        self.accn = accn
        self.locations = locations

class Annotation(Base):
    __tablename__ = 'locate_annotations'
    annot_id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.locate_id'))
    evidence = Column(String(50))
    source_id = Column(Integer(11))
    source_name = Column(String(50))
    accn = Column(String(20))
    locations = relation(Location)

    def __init__(self, evidence, source_id, source_name, accn, locations):
        self.evidence = evidence
        self.source_id = source_id
        self.source_name = source_name
        self.accn = accn
        self.locations = locations

class ExternalReference(Base):
    __tablename__ = 'locate_externalreferences'
    xref_id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.locate_id'))
    source_id = Column(Integer(11))
    source_name = Column(String(50))
    accn = Column(String(20))

    def __init__(self, source_id, source_name, accn):
        self.source_id = source_id
        self.source_name = source_name
        self.accn = accn

class Entry(Base):
    __tablename__ = 'locate_entries'
    locate_id = Column(Integer(11), primary_key=True)
    dbtype = Column(String(30), nullable=True)
    source_name = Column(String(50))
    source_id = Column(Integer(11))
    accn = Column(String(20))
    isoforms = relation(Isoform)
    predictions = relation(Prediction)
    references = relation(Literature)
    annotations = relation(Annotation)
    locations = relation(Location)
    xrefs = relation(ExternalReference)

    def __init__(self, id, source_name, source_id, accn, isoforms, predictions, references, annotations, locations, xrefs, dbtype=None):
        self.locate_id = id
        self.source_name = source_name
        self.source_id = source_id
        self.accn = accn
        self.dbtype = dbtype
        self.isoforms = isoforms
        self.predictions = predictions
        self.references = references
        self.annotations = annotations
        self.locations = locations
        self.xrefs = xrefs
