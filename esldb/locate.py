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
import util.synergizer
import util.proteinlocations

# locations of required eSLDB database files
human = util.proteinlocations.PREFIX + 'eSLDB_Homo_sapiens.txt'
mouse = util.proteinlocations.PREFIX + 'eSLDB_Mus_musculus.txt'

def locate(ensemblgeneid):
	'''
	Returns the locations, urls, and go terms for the protein with
	the specified ensembl gene id

	Parameters
	----------
	*ensemblgeneid

	Return Values
	------------- 
	*ProteinLocations object
	'''

	retval = util.proteinlocations.ProteinLocations()

	# convert the gene id to a peptide id
	peptideids_human = util.synergizer.translate_ensembl_gene_to_ensembl_peptide([ensemblgeneid], 'Homo sapiens')
	peptideids_mouse = util.synergizer.translate_ensembl_gene_to_ensembl_peptide([ensemblgeneid], 'Mus Musculus')

	# search both the mouse and the human
	if peptideids_human[ensemblgeneid] != None:
		for line in file(human):
			retval = processLine(line, peptideids_human, ensemblgeneid, retval)

	if peptideids_mouse[ensemblgeneid] != None:
		for line in file(mouse):
			retval = processLine(line, peptideids_mouse, ensemblgeneid, retval)

	return retval

def processLine(line, peptideids, index, retval):
	url = 'http://www.uniprot.org/uniprot/?query='
	elements = line.strip().split('\t')
	if len(elements) != 11:
		return retval

	_, ensembl_peptide, exp_location, uniprot_location, uniprot_entry, sim_annotation, _, _, prediction, _, _ = elements
	if ensembl_peptide in peptideids[index]:
		# match!
		# hierarchy of terms: first, do we have a URL?
		urlToAdd = ''
		locationToAdd = ''
		if uniprot_entry != 'None':
			urlToAdd = url + uniprot_entry
		else:
			urlToAdd = url + ensembl_peptide

		# second: do we have a location?
		if uniprot_location != 'None':
			locationToAdd = uniprot_location
		elif exp_location != 'None':
			locationToAdd = exp_location
		elif sim_annotation != 'None':
			locationToAdd = sim_annotation
		elif prediction != 'None':
			locationToAdd = prediction
		else:
			locationToAdd = '[No Location Found]'

		# create the entry
		retval.addElement(locationToAdd, '', urlToAdd)

	# done
	return retval
