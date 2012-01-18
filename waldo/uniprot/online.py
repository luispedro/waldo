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
from collections import defaultdict
import urllib
import re

__all__ = ['MUS_MUSCULUS','query']

MUS_MUSCULUS = 'Mus Musculus'
def query(name=None, ensembl=None, gene_name=None, organism=None):
    '''
    locations = query(name=None, ensembl=None, gene_name=None, organism=None):

    Uniprot location for protein, identified by one of:
        - name: Gene or protein name (free-text search)
        - gene_name: Gene name
        - ensembl: Ensembl gene or peptide ID
        - organism: Organism (e.g., 'Mus Musculus' or 'Mouse')
    '''
    # This is based on a Matlab implementation of the same idea by Yanhua

    query = 'reviewed:yes'
    if name:
        query += ' ' + name
    if gene_name:
        query = ' gene:' + gene_name
    if organism:
        query += ' organism:"%s"' % organism
    if ensembl:
        query += ' ensembl %s' % ensembl
    if not query:
        raise ValueError, 'Uniprot.online.query: Empty query'
    accessions = []
    url = 'http://www.uniprot.org/uniprot/?' + urllib.urlencode({'query' : query, 'format':'tab', 'columns':'id'})
    for line in urllib.urlopen(url):
        accessions.append(line.strip())
    results = defaultdict(int)
    for acc in accessions:
        for line in urllib.urlopen('http://www.uniprot.org/uniprot/%s.txt' % acc):
            match = re.search('GO; +GO:([0-9]+);\s*C:([^;]*);',line)
            if match:
                go_nr,go_name = match.groups()
                results[go_name] += 1
    return dict(results)

if __name__ == "__main__":
    print query(ensembl='ENSMUSG00000034254')

