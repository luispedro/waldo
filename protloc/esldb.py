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

flatfile = 'protloc/eSLDB_Mus_musculus.txt'

def locate(value, source = flatfile):
	# loop through the file, searching for value
	retval = {}
	for line in file(flatfile):
		if line.find(value) >= 0:
			# found it!
			key = line.split("\t")[2]
			if key in retval.keys():
				retval[key] += 1
			else:
				retval[key] = 1
	return retval

if __name__ == "__main__":
	print locate('ENSMUSP00000028735')	
