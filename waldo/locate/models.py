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


class Prediction(Base):
    __tablename__ = 'locate_predictions'
    id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.id'), index=True)
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
    id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.id'), index=True)
    literature_id = Column(Integer(11), ForeignKey('locate_literature.id'), nullable=True)
    externalannot_id = Column(Integer(11), ForeignKey('locate_annotations.id'), nullable=True)
    image_id = Column(Integer(11), ForeignKey('locate_images.id'), nullable=True)
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
    id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.id'), index=True)
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
    id = Column(Integer(11), primary_key=True)
    locate_id = Column(Integer(11), ForeignKey('locate_entries.id'), index=True)
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
    locate_id = Column(Integer(11), ForeignKey('locate_entries.id'), index=True)
    source_id = Column(Integer(11))
    source_name = Column(String(50))
    accn = Column(String(20))

    def __init__(self, source_id, source_name, accn):
        self.source_id = source_id
        self.source_name = source_name
        self.accn = accn

class Entry(Base):
    __tablename__ = 'locate_entries'
    id = Column(Integer(11), primary_key=True)
    organism = Column(String(30), nullable=True)
    source_name = Column(String(50))
    source_id = Column(Integer(11))
    accn = Column(String(20))
    isoforms = relation(Isoform)
    predictions = relation(Prediction)
    references = relation(Literature)
    annotations = relation(Annotation)
    locations = relation(Location)
    xrefs = relation(ExternalReference)
    images = relation(Image)

    def __init__(self, id, source_name, source_id, accn, isoforms, predictions, references, annotations, locations, images, xrefs, organism=None):
        self.id = id
        self.source_name = source_name
        self.source_id = source_id
        self.accn = accn
        self.organism = organism
        self.isoforms = isoforms
        self.predictions = predictions
        self.references = references
        self.annotations = annotations
        self.locations = locations
        self.images = images
        self.xrefs = xrefs
