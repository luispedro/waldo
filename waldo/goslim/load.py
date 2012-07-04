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
from models import SlimSet, SlimTerm, SlimMapping
from sqlalchemy.orm import sessionmaker
from os import path

_inputfilename = 'map2MGIslim.txt'


def clear(create_session=None):
    '''
    clear()

    Removes all GO related information
    '''
    from waldo.backend import call_create_session
    session = call_create_session(create_session)
    session.query(SlimSet).delete()
    session.query(SlimTerm).delete()
    session.query(SlimMapping).delete()
    session.commit()


def load(datadir, create_session=None):
    '''
    nr_entries = load(datadir, create_session={backend.create_session})

    Load MGI GO SLIM file

    Parameters
    ----------
      datadir : Directory containing GO files
      create_session : a callable object that returns an sqlalchemy session

    Returns
    -------
      nr_entries : Nr of entries
    '''
    from waldo.backend import call_create_session
    session = call_create_session(create_session)
    filename = path.join(datadir, _inputfilename)
    input = open(filename)

    input.readline() # header
    aspects = {}
    slimset = SlimSet("mgi")
    session.add(slimset)
    loaded = 0
    for line in input:
        go_id,_,slim_id,_ = line.strip().split('\t')
        if slim_id not in aspects:
            term = SlimTerm(slim_id, "mgi")
            session.add(term)
            session.commit()
            aspects[slim_id] = term
        else:
            term = aspects[slim_id]
        mapping = SlimMapping(go_id, term.id)
        session.add(mapping)
        session.commit()
        loaded += 1
    return loaded, len(aspects)
