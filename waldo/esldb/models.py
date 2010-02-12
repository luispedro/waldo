# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base
from backend import Base

class Annotation(Base):
    __tablename__ = 'esldb_annotations'
    annotations_id = Column(Integer(11), primary_key=True)
    entry_id = Column(String(30), ForeignKey('esldb_ids.esldb_id'))
    type = Column(String(30)) # experimental, similarity, predict, etc
    value = Column(String(50))

    def __init__(self, esldb_id, annot_type, annotation):
        self.type = annot_type
        self.value = annotation
        self.entry_id = esldb_id

class UniprotEntry(Base):
    __tablename__ = 'esldb_uniprot_entry'
    uniprot_entry_id = Column(Integer(11), primary_key=True)
    uniprot_entry = Column(String(30))
    entry_id = Column(String(30), ForeignKey('esldb_ids.esldb_id'))

    def __init__(self, esldb_id, uniprot_entry):
        self.uniprot_entry = uniprot_entry
        self.entry_id = esldb_id

class UniprotHomolog(Base):
    __tablename__ = 'esldb_uniprot_homolog'
    uniprot_homolog_id = Column(Integer(11), primary_key=True)
    uniprot_homolog = Column(String(30))
    entry_id = Column(String(30), ForeignKey('esldb_ids.esldb_id'))

    def __init__(self, entryid, homolog):
        self.uniprot_homolog = homolog
        self.entry_id = entryid

class Entry(Base):
    __tablename__ = 'esldb_ids'
    esldb_id = Column(String(30), primary_key=True)
    species = Column(String(30), nullable=False)
    annotations = relation(Annotation)
    uniprot_entries = relation(UniprotEntry)
    uniprot_homologs = relation(UniprotHomolog)

    def __init__(self, esldbid, speciesname):
        self.esldb_id = esldbid
        self.species = speciesname
        self.annotations = []
        self.uniprot_entries = []
        self.uniprot_homologs = []

    def __repr__(self):
        return '<eSLDB %s>' % self.esldb_id
