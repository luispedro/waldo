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
from models import Term
from sqlalchemy.orm import sessionmaker
from os import path

_basedir = path.dirname(path.abspath(__file__))
_inputfilename = path.abspath(path.join(_basedir, '../data/gene_ontology.1_2.obo'))

def load(filename=None, create_session=None):
    '''
    load(filename={data/gene_ontology.1_2.obo}, create_session={backend.create_session})

    Load Gene Ontology OBO file into database

    Parameters
    ----------
      filename : OBO file filename
      create_session : a callable object that returns an sqlalchemy session
    '''
    if filename is None: filename = _inputfilename
    if create_session is None:
        import backend
        create_session = backend.create_session
    session = create_session()

    id = None
    for line in file(filename):
        line = line.strip()
        if line == '[Term]':
            if id is not None and not is_obsolete:
                term = Term(id, name, namespace)
                session.add(term)
            is_a = []
            is_obsolete = False
        if line.find(':') > 0:
            code, content = line.split(':',1)
            content = content.strip()
            if code == 'id':
                id = content
            elif code == 'name':
                name = content
            elif code == 'is_a':
                content,_ = content.split('!')
                content = content.strip()
                is_a.append(content)
            elif code == 'is_obsolete':
                is_obsolete = True
            elif code == 'namespace':
                namespace = content

    session.commit()
