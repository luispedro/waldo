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
from sqlalchemy import and_
from waldo.backend import create_session
from waldo.go.models import Term
import models

def is_cellular_component(go_id, session=None):
    '''
    is_cc = is_cellular_component(go_id, session={new session})

    Returns whether 

    Parameters
    ----------
      go_id : A GO id (e.g., GO:123456789)
    Returns
    -------
      Boolean : whether go_id is in cellular_component namespace
    '''
    if session is None:
        session = create_session()
    return bool( session.query(models.Term) 
                    .filter(and_(
                            models.Term.id == go_id,
                            models.Term.namespace == 'cellular_component'))
                    .count()
                )

def id_to_term(go_id, session=None):
    '''
    term = id_to_term(go_id, session={waldo.backend.create_session()})

    For a GO ID, returns the corresponding term.

    Parameters
    ----------
      go_id : A GO ID (e.g., GO:123456789)
      session : An SQLAlchemy session

    Returns
    -------
      term : A GO term (e.g. "mitochondrion")
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
        A GO ID (e.g., GO:123456789)
    '''
    if session is None: session = create_session()
    term = session.query(Term).filter(Term.name == go_term).first()
    if term is None:
        # if there's no mapping, return the original id
        return go_term
    return term.id

