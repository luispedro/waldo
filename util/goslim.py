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
import util.proteinlocations

# required mapping file
mapfile = util.proteinlocations.PREFIX + 'map2MGIslim.txt'

def map(locationobj):
	'''
	Maps a GO term or ID into its slimmed bin
	* id : GO id (e.g. GO:0000001)
	* term : GO term (e.g. phosphopyruvate hydratase complex)
	'''

	items = locationobj.getResult()
	for line in file(mapfile):
		# loop through the GO terms in the location object
		goterms = items[locationobj.GOIDIDX]
		for i in range(0, len(goterms)):
			if line.find(goterms[i]) >= 0:
				# found something
				bin = line.split("\t")[2]
				locationobj.modifyElementByIndex(i, bin, '', locationobj.getElementByIndex(i)[locationobj.URLIDX])
				
	return locationobj
