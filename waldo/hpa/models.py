# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012, Shannon Quinn <squinn@cmu.edu> and Luis Pedro Coelho <luis@luispedro.org>
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
    entry_id = Column(String(30), ForeignKey('hpa_ids.ensembl_id'), index=True)

    def __init__(self, name, entryid):
        self.name = name
        self.entry_id = entryid

class HPAEntry(Base):
    __tablename__ = 'hpa_ids'
    entry_id = Column(Integer(11), primary_key=True)
    species = Column(String(30))
    ensembl_id = Column(String(50), nullable=False)
    locations = relation(Location)

    def __init__(self, ensembl_id):
        self.species = 'Homo sapiens'
        self.ensembl_id = ensembl_id
        self.locations = []

    def __repr__(self):
        return '<ENSG %s>' % self.ensembl_id

Entry = HPAEntry
