# -*- coding: utf-8 -*-
# Copyright (C) 2009, Shannon Quinn <squinn@cmu.edu>
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
import waldo.util.proteinlocations

# location of REQUIRED database files on the server
associations = waldo.util.proteinlocations.PREFIX + 'gene_association.mgi'
ensembl      = waldo.util.proteinlocations.PREFIX + 'MRK_ENSEMBL.rpt'

def locate(ensemblegeneid):
	'''
	Given an ensembl gene ID, this parses the related MGI files
	to find the locations and generate URLs.

	Parameters
	----------
	*ensemblegeneid

	Return Values
	-------------
	ProteinLocation object

	'''
	url = 'http://www.informatics.jax.org/searchtool/Search.do?query='
	retval = util.proteinlocations.ProteinLocations()
	# first: read the MGI ensembl file to find the query string
	
	for line in file(ensembl):
		mgi_id, _, _, _, _, ensembl_id = line.strip().split('\t')
		# for each line, we have an MGI-specific identifier and
		# the ensembl id
		if ensembl_id == ensemblegeneid:
			# we have our match
			# second: search the annotations file for the 
			# MGI specific id we found in the previous step, 
			# and parse out the location
			for line in file(associations):
				if line[0] == '!' : continue
				elements = line.strip().split('\t')
				mgi = elements[1]
				go_id = elements[4]
				
				# where is the MGI id?
				if mgi == mgi_id:
					# got it
					retval.addElement('', go_id, url + ensembl_id)

	# all done
	return retval
