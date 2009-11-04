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
try:
    import amara
except ImportError:
    print '''Amara is missing.

Amara is a Python package for XML parsing which makes it easier to parse
very large files while keeping memory usage to an acceptable level.

Please install it.'''

from collections import namedtuple
fullfile = 'LOCATE_mouse_v6_20081121.xml'
samplefile = 'LOCATE_sample.xml'

def collect(locatefile):
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

