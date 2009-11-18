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
import sys
from protloc import uniprot
from protloc import esldb
from go import map

def getLocations(key, value):
	'''
	Returns a string indicating how many times the query
	returned a specific result from the given database.
	'''

	# get the locations
	locs_uniprot = uniprot.locate(value)
	locs_esldb = esldb.locate(value)

	# map them
	string = "UNIPROT\n"
	for k, v in locs_uniprot.items():
		mapped = map.mapGo(term = k)
		if mapped:
			string += mapped
		else:
			string += k
		string += "(%s)\n" % v

	string += "\neSLDB\n"
	for k, v in locs_esldb.items():
		mapped = map.mapGo(term = k)
		if  mapped:
			string += mapped
		else:
			string += k
		string += "(%s)\n" % v

	# done
	return string

if __name__ == "__main__":
	#print getLocations(sys.argv[1], sys.argv[2])
	print getLocations('ensembl', 'ENSMUSG00000034254')
