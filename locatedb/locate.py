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
import amara

human = util.proteinlocations.PREFIX + 'LOCATE_human_v6_20081121_SAMPLE.xml'
mouse = util.proteinlocations.PREFIX + 'LOCATE_mouse_v6_20081121_SAMPLE.xml'

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

def parseXML(ensemblid, file, retval):
	url = 'http://www.ncbi.nlm.nih.gov/pubmed/'
	for protein in amara.pushbind(file, u'LOCATE_protein'):
		# first, is this the droid we're looking for?
		refs = protein.xml_xpath('xrefs//accn')
		if ensemblid in refs:
			# found the correct element, extract the info
			locations = protein.xml_xpath('literature//location[@goid]')
			citations = protein.xml_xpath('literature//accn')
			for citation in citations:
				# for each citation, list the locations
				for location in locations:
					goids = location.goid.split(';')
					for g in goids:
						# add the element
						retval.addElement('', g, url + str(citation))
			
	return retval
