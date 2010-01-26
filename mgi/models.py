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

class GOAnnotation(Base):
    __tablename__ = 'mgi_goannotation'
    mgi_go_id = Column(Integer, primary_key=True)
    mgi_id = Column(String(32), ForeignKey('mgi_entry.mgi_id'))
    go_id = Column(Integer(7), nullable=False)
    pubmedid = Column(Integer(11))
    evidence = Column(String(3), nullable=True)

    def __init__(self, mgi_id, go_id, pubmedid=None, evidence=None):
        self.mgi_id = mgi_id
        self.go_id = go_id
        self.pubmedid = pubmedid
        self.evidence = evidence

class Entry(Base):
    __tablename__ = 'mgi_entry'
    mgi_id = Column(String(32), nullable=False, primary_key=True)
    name = Column(String(32))
    annotations = relation(GOAnnotation)

    def __init__(self, mgi_id, name):
        self.mgi_id = mgi_id
        self.name = name
        self.annotations = []

    def __repr__(self):
        return '<%s>' % self.mgi_id

