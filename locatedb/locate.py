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
import util.proteinlocations
import util.synergizer
import re

human = util.proteinlocations.PREFIX + 'LOCATE_human_v6_20081121.xml'
mouse = util.proteinlocations.PREFIX + 'LOCATE_mouse_v6_20081121.xml'

def locate(ensemblgeneid):
	'''

	Parameters
	----------
	*ensemblgeneid

	Return Value
	------------
	*ProteinLocation object

	'''
	retval = util.proteinlocations.ProteinLocations()

	# use of the synergizer is somewhat of a tricky optimization hack
	# to see if we really need to parse both XML files
	peptide_mice = util.synergizer.translate_ensembl_gene_to_ensembl_peptide([ensemblgeneid], 'Mus musculus')
	peptide_humans = util.synergizer.translate_ensembl_gene_to_ensembl_peptide([ensemblgeneid], 'Homo sapiens')

	if peptide_mice[ensemblgeneid] != None:
		retval = parseXML(ensemblgeneid, mouse, retval)

	if peptide_humans[ensemblgeneid] != None:
		retval = parseXML(ensemblgeneid, human, retval)	

	return retval

def parseXML(ensemblid, filename, retval):
	literature = ''
	inliterature = 0
	inxrefs = 0
	header = ''
	xrefs = ''
	#url = 'http://www.ncbi.nlm.nih.gov/pubmed/'
	url = 'http://locate.imb.uq.edu.au/cgi-bin/report.cgi?entry='	

	# line by line!
	for line in file(filename):
        	# first, all the checks for where we might be
		if line.find('<LOCATE_protein') >= 0:
			header = line
		elif line.find('<literature>') >= 0:
			inliterature = 1
		elif line.find('</literature>') >= 0:
			inliterature = 0
		elif line.find('<xrefs>') >= 0:
			inxrefs = 1
		elif line.find('</xrefs>') >= 0:
			# at this state, we have all the info we need
			inxrefs = 0
			# start the search for the ensemblid
			if xrefs.find(ensemblid) >= 0:
				# found it
				#citations = re.search('<accn>([0-9]*)</accn>', literature)
				citations = re.search('uid="([0-9]*)"', header)
				goterms = re.search('(GO:[0-9]+)+;*(GO:[0-9]+)*', literature)
				if citations and goterms:
					cite = citations.groups()
					goids = goterms.groups()
					for goid in goids:
						if goid != None:
							retval.addElement('', goid, url + cite[0])
			# start over!
			literature = ''
			xrefs = ''
			header = ''

		# now, check what state we're in and act accordingly
		if inxrefs == 1:
			xrefs += line
		if inliterature == 1:
			literature += line
	
	return retval
