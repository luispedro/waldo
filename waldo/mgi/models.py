# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012, Luis Pedro Coelho <luis@luispedro.org>
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
from waldo.backend import Base

class GOAnnotation(Base):
    __tablename__ = 'mgi_goannotation'
    mgi_go_id = Column(Integer, primary_key=True)
    mgi_id = Column(String(32), ForeignKey('mgi_entry.mgi_id'), index=True)
    go_id = Column(String(15), nullable=False)
    evidence_code = Column(String(3), nullable=True)
    evidence = Column(String(3), nullable=True)

    def __init__(self, mgi_id, go_id, evidence_code, evidence=None):
        self.mgi_id = mgi_id
        self.go_id = go_id
        self.evidence_code = evidence_code
        self.evidence = evidence

class MGIEntry(Base):
    __tablename__ = 'mgi_entry'
    mgi_id = Column(String(32), nullable=False, primary_key=True)
    name = Column(String(32))
    pubmedids = Column(String(100), nullable=True)
    go_annotations = relation(GOAnnotation)
    references = []
    organisms = [u'Mus Musculus']

    @property
    def internal_id(self):
        return self.mgi_id

    def __init__(self, mgi_id, name):
        self.mgi_id = mgi_id
        self.name = name
        self.go_annotations = []

    def __repr__(self):
        return '<%s>' % self.mgi_id

Entry = MGIEntry
