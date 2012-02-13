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
from sqlalchemy.ext.declarative import declarative_base
from waldo.backend import Base

class Term(Base):
    __tablename__ = 'go_term'
    id = Column(String(24), primary_key=True)
    name = Column(String(32))
    namespace = Column(String(64))

    def __init__(self, id, name, namespace):
        assert id.startswith('GO:'), 'waldo.go.models: Invalid GO-ID'
        self.id = id
        self.name = name
        self.namespace = namespace

    def __str__(self):
        return '<GO Model %s ("%s")>' % (self.id, self.name)

    def __unicode__(self):
        return unicode(str(self))

class TermRelationship(Base):
    __tablename__ = 'go_term_relationship'
    id = Column(Integer, primary_key=True)
    from_term = Column(String(24), ForeignKey('go_term.id'))
    to_term = Column(String(24), ForeignKey('go_term.id'))
    relname = Column(String(24))

    def __init__(self, from_term, to_term, relname):
        self.from_term = from_term
        self.to_term = to_term
        self.relname = relname

