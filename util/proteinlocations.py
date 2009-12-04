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

# global prefix for where all database files can be found on the filesystem
#PREFIX = '/pslid/databases/'
PREFIX = '/home/squinn/databases/'

class ProteinLocations:

	def __init__(self):
		# initialize the dictionary of dictionaries
		self.LOCATIONIDX = 'locations'
		self.URLIDX = 'urls'
		self.GOIDIDX = 'goids'
		self.collection = {
				self.LOCATIONIDX: [],
				self.URLIDX: [],
				self.GOIDIDX: [],
				}

	def addElement(self, location, goid, url):
		self.collection[self.LOCATIONIDX].append(location)
		self.collection[self.URLIDX].append(url)
		self.collection[self.GOIDIDX].append(goid)

	def getElementByGoId(self, goid):
		if goid in self.collection[self.GOIDIDX]:
			idx = self.collection[self.GOIDIDX].index(goid)
			return self.getElementByIndex(idx)
		return {}

	def getElementByIndex(self, index):
		if index in range(0, len(self.collection[self.LOCATIONIDX])):
			return {
				self.LOCATIONIDX: self.collection[self.LOCATIONIDX][index],
				self.GOIDIDX: self.collection[self.GOIDIDX][index],
				self.URLIDX: self.collection[self.URLIDX][index],
				}
		return {}

	def modifyElementByIndex(self, index, location, goid, url):
		self.collection[self.LOCATIONIDX][index] = location
		self.collection[self.GOIDIDX][index] = goid
		self.collection[self.URLIDX][index] = url

	def removeElementByIndex(self, index):
		del self.collection[self.LOCATIONIDX][index]
		del self.collection[self.GOIDIDX][index]
		del self.collection[self.URLIDX][index]

	def getResult(self):
		return self.collection
