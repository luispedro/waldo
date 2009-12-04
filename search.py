# -*- coding: utf-8 -*-
# Copyright (C) 2009, Shannon Quinn <squinn@cmu.edu>
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
import esldb.locate
import uniprot.locate
import mgi.locate
import locatedb.locate
import util.proteinlocations
import util.goslim

AVAILABLE_DATABASES = {
			'esldb':'eSLDB',
			'uniprot':'Uniprot',
			'mgi':'MGI',
			'locatedb':'LOCATE',
			}

def locate(ensemblgeneid):
	'''
	Returns a string indicating how many times the query
	returned a specific result from the given database.

	Parameters
	---------
	*ensemblegeneid: An ensembl gene ID
		NOTE: There are multiple types of ensembl IDs;
			transcript, peptide, and gene. Make sure
			this is a GENE ID.

	Return Value
	------------
	*a dictionary of results, organized by database
	'''
	retval = {}
	for k in AVAILABLE_DATABASES.iterkeys():
		results = None
		if k == 'esldb':
			results = esldb.locate.locate(ensemblgeneid)
		elif k == 'locatedb':
			results = locatedb.locate.locate(ensemblgeneid)
		elif k == 'uniprot':
			results = uniprot.locate.locate(ensemblgeneid)
		elif k == 'mgi':
			results = mgi.locate.locate(ensemblgeneid)

		# map the go-slim terms
		results = util.goslim.map(results)

		# TODO - optimize results
		results = optimize(results)

		# add go-slimmed result to final return value
		retval[k] = results.getResult()
	return retval

def optimize(locationobj):
	'''
	Performs various optimizations on the data.
	'''

	# FIXME
	return locationobj

if __name__ == "__main__":
	#locate('ENSMUSG00000026004')
	locate('ENSMUSG00000049553')
