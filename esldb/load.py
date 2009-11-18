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

def collect(esldbfile):
	first = 0
	indices = {"0":"eSLDB code", 
		"1":"Original Database Code",
		"2":"Experimental Annotation",
		"3":"Swissprot Fulltext Annotation",
		"4":"Swissprot Entry",
		"5":"Similarity-based Annotation",
		"6":"Swissprot Homologue",
		"7":"E-value",
		"8":"Prediction",
		"9":"Aminoacidic Sequence",
		"10":"Common Name"}
	indices = []
	entries = []
	for line in file(esldbfile):
		li = line.split("\t")
		if first == 0:
			first = 1
			indices = li[:]
		else:
			# capture the information about this entry
			entries.append(li)
				
	# given each item, let's collect statistics
	for entry in entries:
		if len(entry) > 3:
			print entry[2]
			print entry[3]
			print entry[4]

if __name__ == "__main__":
	collect("../../datasets/ESLDB_MOUSE.txt")
