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
import re

goslim = "go/map2MGIslim.txt"

def mapGo(id=None, term=None):
	'''
	Maps a GO term or ID into its slimmed bin
	* id : GO id (e.g. GO:0000001)
	* term : GO term (e.g. phosphopyruvate hydratase complex)
	'''
	for line in file(goslim):
		query = ''
		if id:
			query = id
		else:
			query = term
		if line.find(query) >= 0:
			# found something
			return line.split("\t")[2]
	return None

if __name__ == "__main__":
	print mapGo(term = "lollers")
