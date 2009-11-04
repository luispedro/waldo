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
import numpy as np
import amara
import networkx as nx

def _getgo(r):
    prefix = u'http://www.geneontology.org/go#'
    if not r.startswith(prefix):
        raise ValueError, "go.load._getgo: Don't know what to do with %s" % r
    return r[len(prefix):]
G = nx.DiGraph()
root = amara.parse('go_daily-termdb.rdf-xml')
terms = root.xml_xpath('//go:term')
for term in terms:
    G.add_node(unicode(term.accession))
    if hasattr(term, 'is_a'):
        for isa in term.is_a:
            G.add_edge(unicode(term.accession), _getgo(isa.resource))
            
G.name = 'Gene Ontology'
cc_root = 'GO:0005575'
q = set(G.predecessors(cc_root))
seen = set()
while q:
    next = q.pop()
    seen.add(next)
    neighbours = G.predecessors(next)
    for n in neighbours:
        if n not in seen:
            q.add(n)
