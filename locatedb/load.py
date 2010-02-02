# -*- coding: utf-8 -*-
# Copyright (C) 2009, Luís Pedro Coelho <lpc@cmu.edu>
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
import amara
import models
from os import path
from collections import defaultdict
from translations.models import Translation

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../data'))

#_mouse = 'LOCATE_mouse_v6_20081121.xml'
#_human = 'LOCATE_human_v6_20081121.xml'
_mouse = 'LOCATE_mouse_v6_20081121_SMALL.xml'
_human = 'LOCATE_human_v6_20081121_SMALL.xml'

def load(dirname=None, create_session=None):
    '''
    num_entries = load(dirname={data/}, create_session={backend.create_session})

    Load LOCATE database file information into local relational database

    Parameters
    ----------
      dirname : System folder containing database files
      create_session : Callable object which returns an sqlalchemy session

    Returns
    -------
      num_entries : Number of entries loaded into the local database

    References
    ----------
        To download database files:
        http://locate.imb.uq.edu.au/downloads.shtml
    '''
    if dirname is None: dirname = _datadir
    if create_session is None:
        import backend
        create_session = backend.create_session
    session = create_session()

    # load the mouse and human separately
    mouse_loaded = _loadfile(path.join(dirname, _mouse), session)
    human_loaded = _loadfile(path.join(dirname, _human), session)

    return len(mouse_loaded) + len(human_loaded)

def _loadfile(filename, session):
    entries = set()
    count = 0
    # LOCATE doesn't define a namespace, so we don't need prefix information ?
    for entry in amara.pushbind(filename, u'LOCATE_protein'):
        count += 1


def collect(locatefile = fullfile):
    locations = set()
    protein_records = 0
    with_location = 0
    images = 0
    coloc_images = 0

    for protein in amara.pushbind(locatefile, u'LOCATE_protein'):
        protein_records += 1
        curlocations = protein.xml_xpath('literature//location[@goid]')
        if curlocations:
            with_location += 1
        for location in curlocations:
            goids = location.goid.split(';')
            for g in goids:
                locations.add(g)
        if unicode(protein.experimental_data.images).strip():
            images += 1
        if unicode(protein.experimental_data.coloc_images).strip():
            coloc_images += 1

    print 'Protein records:', protein_records
    print 'Protein records with literature records:', with_location
    print 'With image record:', images
    print 'With colocalisation record:', coloc_images
    print 'Different locations used:', len(locations)

