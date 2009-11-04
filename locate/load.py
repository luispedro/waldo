# -*- coding: utf-8 -*-
# Copyright (C) 2009, Luís Pedro Coelho <lpc@cmu.edu>
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
import cPickle as pickle
import gzip
from lxml import etree

labels = {}
locations = {}
for event, node in etree.iterparse('LOCATE_mouse_v6_20081121.xml'):
    if node.find('literature') is not None:
        key = node.findtext('protein/source/accn')
        locs = []
        for n in node.findall('literature/reference/locations/location'):
            locs.append([nn.text for nn in n.getchildren()])
        locations[key] = locs
        print len(locations)
        node.clear()

pickle.dump((labels,locations),gzip.GzipFile('labelslocations.pp.gz','w'))
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
