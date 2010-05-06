# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base
from waldo.backend import Base

class Location(Base):
    __tablename__  = 'hpa_location'
    loc_id = Column(Integer(11), primary_key=True)
    name = Column(String(30), nullable=False)
    entry_id = Column(String(30), ForeignKey('hpa_ids.hpa_id'), index=True)

    def __init__(self, name, entryid):
        self.name = name
        self.entry_id = entryid

class Entry(Base):
    __tablename__ = 'hpa_ids'
    entry_id = Column(Integer(11), primary_key=True)
    hpa_id = Column(String(30), nullable=False)
    cell_line = Column(String(30), nullable=False)
    species = Column(String(30))
    ensembl_id = Column(String(50), nullable=False)
    locations = relation(Location)

    def __init__(self, antibodyid, ensembl_id, cell_line):
        self.hpa_id = antibodyid
        self.species = 'Homo sapiens'
        self.ensembl_id = ensembl_id
        self.cell_line = cell_line
        self.locations = []

    def __repr__(self):
        return '<HPA %s>' % self.hpa_id
