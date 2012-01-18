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
from models import SlimSet, SlimTerm, SlimMapping

def map_to_goslim(go_id, set_name, session=None):
    '''
    go_slim_term = map_to_goslim(go_id, set_name, session={backend.create_session()})

    Map a GO term to a GO slim term in sub-vocabulary `set_name`

    Parameters
    ----------
    go_id : string
        GO id
    set_name : string
        name of GO Slim to use
    session : sqlalchemy session, optional
        sqlalchemy session (default : `backend.create_session()`)

    Returns
    -------
    go_slim_term : str or None
        GO Slim Term corresponding to input `go_id`
    '''
    if session is None:
        from waldo.backend import create_session
        session = create_session()
    entry = (session.query(SlimTerm)
                    .join(SlimMapping)
                    .join(SlimSet)
                    .filter(SlimSet.id == set_name)
                    .filter(SlimMapping.full_id == go_id)
                    .first())
    if entry is None: return None
    return entry.name

