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
from sqlalchemy import and_
from waldo.backend import create_session
from waldo.go.models import Term, TermRelationship
import models

def is_cellular_component(go_id, session=None):
    '''
    is_cc = is_cellular_component(go_id, session={new session})

    Returns whether the id belongs to the cellular component sub-ontology

    Parameters
    ----------
    go_id : str
        A GO id (e.g., GO:123456789)
    session : SQLAlchemy session object, optional

    Returns
    -------
    is_cc : Boolean
        whether go_id is in cellular_component namespace
    '''
    return (vocabulary(go_id, session) == 'cellular_component')


def vocabulary(go_id, session=None):
    '''
    voc = vocabulary(go_id, session={new session})

    Return the vocabulary to which the `go_id` belongs.

    Parameters
    ----------
    go_id : str
        A GO id (e.g., GO:123456789)
    session : SQLAlchemy session object, optional

    Returns
    -------
    voc: str
        Vocabulary (one of 'cellular_component', 'molecular_process', 'biological_function')
        None if not found.
    '''
    if session is None:
        session = create_session()
    entry = session.query(models.Term) \
                    .filter(models.Term.id == go_id) \
                    .first()
    if entry:
        return entry.namespace


def id_to_term(go_id, session=None):
    '''
    term = id_to_term(go_id, session={waldo.backend.create_session()})

    For a GO ID, returns the corresponding term.

    Parameters
    ----------
    go_id : str
        A GO ID (e.g., GO:0005739)
    session :  SQLAlchemy session object, optional

    Returns
    -------
    term : str
        A GO term (e.g. "mitochondrion")
    '''
    if session is None: session = create_session()
    term = session.query(Term).filter(Term.id == go_id).first()
    if term is None:
        # if there's no mapping, return the original id
        return go_id
    else:
        return term.name

def term_to_id(go_term, session=None):
    '''
    go_id = term_to_id(go_term, session={waldo.backend.create_session()})

    For a GO term, returns the corresponding ID.

    If no ID is found, returns the original term.

    Parameters
    ----------
    term : string
        A GO term (e.g. "mitochondrion")
    session : SQLAlchemy session, optional

    Returns
    -------
    go_id : string
        A GO ID (e.g., GO:0005739)
    '''
    if session is None: session = create_session()
    term = session.query(Term).filter(Term.name == go_term).first()
    if term is None:
        # if there's no mapping, return the original id
        return go_term
    return term.id


def related(term, level=1, create_session=None):
    '''
    for relname, to_term in related(term, create_session={backend.create_session}):
        ....

    Parameters
    ----------
    term : str or unicode
        GO term
    level : int, optional
        Maximum recursion level. Use ``-1`` for infinite recursion
    create_session : callable

    Returns
    -------
    iterator
    '''
    if create_session is None:
        from waldo.backend import create_session
    session = create_session()
    seen = set()
    def recurse(term, level):
        if level == 0:
            return
        q = session\
            .query(TermRelationship)\
            .filter_by(from_term=term)
        for rel in q.all():
            if rel.to_term not in seen:
                seen.add(rel.to_term)
                recurse(rel.to_term, level-1)
    recurse(term, level)
    for r in seen:
        yield r

