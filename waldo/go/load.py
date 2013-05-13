# -*- coding: utf-8 -*-
# Copyright (C) 2009-2013, Luis Pedro Coelho <luis@luispedro.org>
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
from sqlalchemy.orm import sessionmaker
from os import path

from models import Term, TermRelationship
from waldo.tools import _gzip_open

_inputfilename = 'gene_ontology.1_2.obo'

def clear(create_session=None):
    '''
    clear()

    Removes all GO related information
    '''
    from waldo.backend import call_create_session
    from . import models
    session = call_create_session(create_session)
    session.query(models.Term).delete()
    session.query(models.TermRelationship).delete()
    session.commit()


def _parse_terms(stream):
    from collections import defaultdict
    in_term = False
    for line in stream:
        line = line.strip()
        if not line:
            if in_term:
                yield term
            in_term = False
            continue
        if line == '[Term]':
            in_term = True
            term = defaultdict(list)
        if in_term:
            key,_,value = line.partition(':')
            value = value.strip()
            if key == 'is_a':
                value,_,_ = value.partition(' ! ')
            elif key == 'relationship':
                content = value.split()
                if content[0] == 'part_of':
                    key = 'part_of'
                    value = content[1]
            term[key].append(value)

def load(datadir, create_session=None):
    '''
    nr_entries = load(datadir, create_session={backend.create_session})

    Load Gene Ontology OBO file into database

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
    if not path.exists(filename) and path.exists(filename + '.gz'):
        input = _gzip_open(filename)
    else:
        input = open(filename)

    id = None
    in_term = False
    loaded = 0
    for term in _parse_terms(input):
        if term['is_obsolete']:
            continue
        session.add(
            Term(id=term['id'][0], name=term['name'][0], namespace=term['namespace'][0]))
        for rel in ('is_a','part_of'):
            for t in term[rel]:
                r = TermRelationship(id, t, rel)
                session.add(r)
        loaded += 1
        # This check is ugly, but commit() is rather slow
        # The speed up is worth it:
        if (loaded % 512) == 0:
            session.commit()
    session.commit()
    return loaded
