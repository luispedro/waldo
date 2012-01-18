# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <luis@luispedro.org>
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
from waldo.go.models import Term as GOTerm

class SlimSet(Base):
    __tablename__ = 'go_slim_set'
    id = Column(String(24), primary_key=True)

    def __init__(self, id):
        self.id = id

class SlimTerm(Base):
    __tablename__ = 'go_slim_term'
    id = Column(Integer, primary_key=True)
    name = Column(String(24))
    slim_set = Column(String(24), ForeignKey('go_slim_set.id'))

    def __init__(self, name, slim_set):
        self.name = name
        self.slim_set = slim_set

class SlimMapping(Base):
    __tablename__ = 'go_slim_map'
    id = Column(Integer, primary_key=True)
    full_id = Column(String(24), ForeignKey(GOTerm.id), index=True)
    slim_id = Column(String(24), ForeignKey(SlimTerm.id))

    def __init__(self, full_id, slim_id):
        self.full_id = full_id
        self.slim_id = slim_id


