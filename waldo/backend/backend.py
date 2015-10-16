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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import path
import logging

logging = logging.getLogger('backend')

_paths = [
    '.',
    path.expanduser('~/.local/share/waldo'),
    path.join(path.abspath(path.dirname(__file__)), '..', '..'),
    '/var/lib/waldo',
    ]
Base = declarative_base()
use_fts = False
_engine = None
_create_session = None

_waldo_database_version = '2013-09-10'

def init(database_file=None, reinit=False):
    global _engine, _create_session
    basename = 'waldo.sqlite3'
    creating = False
    if database_file is None:
        for basep in _paths:
            fullp = path.join(basep, basename)
            if path.exists(fullp):
                database_file = fullp
                logging.info('Using database: %s' % database_file)
                break
        else:
            database_file = path.join(_paths[0], basename)
    if reinit:
        from os import unlink
        try:
            unlink(database_file)
        except:
            pass
    creating = not path.exists(database_file)
    _engine = create_engine('sqlite:///' + database_file, echo=False)
    _create_session = sessionmaker(bind=_engine)
    conn = _engine.connect()
    if creating:
            conn.execute('CREATE TABLE waldo_version (waldo_version_created CHAR(255))')
            conn.execute('INSERT INTO waldo_version VALUES ("%s")' % _waldo_database_version)
    else:
        (v,) = conn.execute('SELECT * FROM waldo_version')
        if v[0] != _waldo_database_version:
            raise KeyError('Database version mismatch (using file `%s`)' % database_file)

def create_session(**kwargs):
    '''
    session = create_session(**kwargs)

    Parameters
    ---
    kwargs : any
        If used, these are passed as **kwargs to the session maker
    '''
    if _create_session is None:
        init()
    return _create_session(**kwargs)

def call_create_session(creator):
    '''
    session = call_create_session(creator)

    if creator is not None, calls it; otherwise, uses the global create_session
    '''
    if creator: return creator()
    return create_session()

def create_tables(build_fulltext_index=False):
    '''
    create_tables(build_fulltext_index=False)

    Creates all tables in database.

    Parameters
    ----------

    build_fulltext_index : bool, optional
        Whether to build the full-text index (default: False)
    '''
    metadata = Base.metadata
    metadata.bind = _engine
    metadata.create_all()
    conn = _engine.connect()
    if build_fulltext_index:
        global use_fts
        use_fts = True
        #drop the old uniprot organism entry, and create a virtual one with fts4
        conn.execute("drop table uniprot_entry")
        conn.execute("""CREATE VIRTUAL TABLE uniprot_entry USING fts4 (
                name VARCHAR(32) NOT NULL,
                rname VARCHAR(128) NOT NULL,
                gname VARCHAR(128) NOT NULL,
                sequence TEXT,
                PRIMARY KEY (name))""")


