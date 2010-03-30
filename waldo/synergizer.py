# -*- coding: utf-8 -*-
# Copyright (C) 2009, Luis Pedro Coelho <lpc@cmu.edu>
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
import urllib2
import json 

def jsonrpc(url, method, args):
    '''
    result = jsonrpc(url, method, args)

    Make a JSON-RPC call through HTTP to URL url.

    Implements version 1.0 of the protocol.

    Reference: http://en.wikipedia.org/wiki/JSON-RPC
    '''
    dataenc = json.dumps({'method':method,'params':args, 'id':'me'})
    req = urllib2.Request(url='http://llama.med.harvard.edu/cgi/synergizer/serv', data=dataenc, headers={'content-Type':'application/json'})
    result = urllib2.urlopen(req).read()
    result = json.loads(result)
    if result['error']:
        raise IOError, result['error']
    return result['result']

_SYNERGIZER_URL = 'http://llama.med.harvard.edu/cgi/synergizer/serv'

def translate_ensembl_gene_to_ensembl_peptide(ids, organism='Mus Musculus'):
    '''
    results = translate_ensembl_gene_to_ensembl_peptide(ids, organism='Mus Musculus')

    Translate ensembl gene to ensembl peptide IDs.
    
    Parameters
    ----------
        * ids: List of strings to translate
        * organism: Organism (default: 'Mus Musculus')

    Results is a *dictionary* that maps *id* to a **list** of ids
        (because of alternative splicing, each gene can map to one or more proteins)
        or to None if no mapping was found.
    '''
    data = {
        'authority': 'ensembl',
        'species'  : organism,
        'domain'   : 'ensembl_gene_id',
        'range'    : 'ensembl_peptide_id',
        'ids'      : ids,
    }
    results = {}
    for r in jsonrpc(_SYNERGIZER_URL,'translate',[data]):
        k = r[0]
        vs = r[1:]
        if len(vs) == 1 and vs[0] is None:
            vs = None
        results[k] = vs
    return results

def translate_ensembl_peptide_to_ensembl_gene(ids, organism='Mus Musculus'):
    '''
    results = translate_ensembl_peptide_to_ensembl_gene(ids, organism='Mus Musculus')

    Translates ensembl peptide IDs to ensembl gene IDs.

    Parameters
    ----------
      ids: List of strings to translate
      organism: The organism (default: Mus Musculus)

    Results
    -------
      result: A dict of gene IDs, the key of which in the list corresponds
      to the peptide ID in the list of peptides. At this time, it is believed 
      that a peptide ID maps to one gene ID.
    '''
    
    data = {
        'authority': 'ensembl',
        'species'  : organism,
        'domain'   : 'ensembl_peptide_id',
        'range'    : 'ensembl_gene_id',
        'ids'      : ids,
    }
    results = {}
    for r in jsonrpc(_SYNERGIZER_URL,'translate',[data]):
        k = r[0]
        vs = r[1:]
        results[k] = vs[0]
    return results
    
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:

