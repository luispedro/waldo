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
    __tablename__ = 'esldb_ids'
    esldb_id = Column(String(30), primary_key=True)
    species = Column(String(30), nullable=False)

    def __init__(self, esldbid, speciesname):
        self.esldb_id = esldbid
        self.species = speciesname

    def __repr__(self):
        return '<eSLDB %s>' % self.esldb_id

class Annotation(Base):
    __tablename__ = 'esldb_annotations'
    entry_id = Column(String(30), ForeignKey('esldb_ids.esldb_id'))
    type = Column(String(30), primary_key=True)
    value = Column(String(50), primary_key=True)

    def __init__(self, entry, annot_type, annotation):
        self.entry_id = entry
        self.type = annot_type
        self.value = annotation

class UniprotEntry(Base):
    __tablename__ = 'esldb_uniprot_entry'
    uniprot_entry = Column(String(30), primary_key=True)
    entry_id = Column(String(30), primary_key=True, ForeignKey('esldb_ids.esldb_id'))

    def __init__(self, entryid, entry):
        self.entry_id = entryid
        self.uniprot_entry = entry

class UniprotHomolog(Base):
    __tablename__ = 'esldb_uniprot_homolog'
    uniprot_homolog = Column(String(30), primary_key=True)
    entry_id = Column(String(30), primary_key=True, ForeignKey('esldb_ids.esldb_id'))

    def __init__(self, entryid, homolog):
        self.entry_id = entryid
        self.uniprot_homolog = homolog
