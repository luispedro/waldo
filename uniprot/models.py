# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
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

class Accession(Base):
    __tablename__ = 'uniprot_accession'
    uniprot_name = Column(String, ForeignKey('uniprot_entry.name'))
    accession = Column(String, nullable=False, primary_key=True)

    def __init__(self, accession):
        self.accession = accession

class Reference(Base):
    __tablename__ = 'uniprot_reference'
    uniprot_name = Column(String, ForeignKey('uniprot_entry.name'))
    refid = Column(Integer, primary_key=True)
    key = Column(String)
    type = Column(String)
    title = Column(String)

    def __init__(self, key, type, title):
        self.type = type
        self.key = key
        self.title = title

class Comment(Base):
    __tablename__ = 'uniprot_comment'
    uniprot_name = Column(String, ForeignKey('uniprot_entry.name'))
    commentid = Column(Integer, primary_key=True)
    type = Column(String)
    text = Column(String)

    def __init__(self, type, text):
        self.type = type
        self.text = text

class Entry(Base):
    __tablename__ = 'uniprot_entry'
    name = Column(String, nullable=False, primary_key=True)
    accessions = relation(Accession)
    references = relation(Reference)
    comments = relation(Comment)

    def __init__(self, name, accessions, comments, references):
        self.name = name
        if type(accessions[0]) in (str, unicode):
            accessions = map(Accession, accessions)
        self.accessions = accessions
        self.references = references
        self.comments = comments

    def __repr__(self):
        return '<Uniprot Entry: %s>' % self.name

