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

AVAILABLE_DATABASES = [
			'esldb',
#			'uniprot',
#			'mgi',
#			'locatedb',
			]

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
	for k in AVAILABLE_DATABASES:
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
	Performs various optimizations on the data. Specifically:
	many times the same ID will appear multiple times or return
	multiple hits, all of which reduce to the same location
	and URL. Rather than repeat these two items 12 separate times
	as independent hits, we'll strip out all but 1.

	Parameters
	----------
	*locationobj A ProteinLocation object

	Return Value
	------------
	*optimized ProteinLocation object
	'''

	length = len(locationobj.getResult()[locationobj.LOCATIONIDX])
	todelete = []
	for i in range(0, length):
		for j in range(i, length):
			if i != j:
				# get the two elements
				one = locationobj.getElementByIndex(i)
				two = locationobj.getElementByIndex(j)
				
				# compare them - are they the same?
				if one[locationobj.LOCATIONIDX] == two[locationobj.LOCATIONIDX] and one[locationobj.URLIDX] == two[locationobj.URLIDX]:
					# yes they are: mark one of them for deletion
					if i not in todelete:
						todelete.append(i)

	# go through the delete array, deleting those indices
	for delindex in reversed(todelete):
		locationobj.removeElementByIndex(delindex)

	return locationobj

if __name__ == "__main__":
	count = 0
	input = '/home/squinn/ensembl_ids.txt'
	f = open('/home/squinn/protein_locator/output.txt', 'w')
	for line in file(input):
		count += 1
		item = line.strip()
		retval = locate(item)
		output = item
		if 'uniprot' in AVAILABLE_DATABASES and len(retval['uniprot']['locations']) > 0:
			output += ',' + retval['uniprot']['locations'][0] + ',' + retval['uniprot']['urls'][0]
		else:
			output += ',None,None' 

		if 'esldb' in AVAILABLE_DATABASES and len(retval['esldb']['locations']) > 0:
			output += ',' + retval['esldb']['locations'][0].replace(',', ';') + ',' + retval['esldb']['urls'][0]
		else:
			output += ',None,None'

		if 'mgi' in AVAILABLE_DATABASES and len(retval['mgi']['locations']) > 0:
			output += ',' + retval['mgi']['locations'][0] + ',' + retval['mgi']['urls'][0]
		else:
			output += ',None,None'

		if 'locatedb' in AVAILABLE_DATABASES and len(retval['locatedb']['locations']) > 0:
			output += ',' + retval['locatedb']['locations'][0] + ',' + retval['locatedb']['urls'][0]
		else:
			output += ',None,None'
		print output
		f.write(output + '\n')
		#if count == 20:
		#	break
	f.close()
