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
import numpy as np
import urllib
import re
import util.proteinlocations

__all__ = ['MUS_MUSCULUS','locate']

MUS_MUSCULUS = 'Mus Musculus'
def locate(ensemblgeneid):
	'''
	locations = locate(ensemblgeneid):

	Uniprot location for protein, identified by:
	* ensemblgeneid: Ensembl gene ID
	'''

	# This is based on the Uniprot locate code by Luis Pedro Coelho
	query = 'reviewed:yes'
        query += ' ensembl %s' % ensemblgeneid
	accessions = []
	url = 'http://www.uniprot.org/uniprot/?' + urllib.urlencode({'query' : query, 'format':'tab', 'columns':'id'})
	for line in urllib.urlopen(url):
		accessions.append(line.strip())
	results = util.proteinlocations.ProteinLocations()
	for acc in accessions:
		url = 'http://www.uniprot.org/uniprot/'
		for line in urllib.urlopen(url + '%s.txt' % acc):
			match = re.search('GO; +GO:([0-9]+);\s*C:([^;]*);',line)
			if match:
				go_nr,go_name = match.groups()
				results.addElement(go_name, go_nr, url + acc)
	return results

# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
