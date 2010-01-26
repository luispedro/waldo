# -*- coding: utf-8 -*-
# Copyright (C) 2009, Luís Pedro Coelho <lpc@cmu.edu>
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
from collections import defaultdict 
import models

def load(filename, create_session):
    '''
    load(filename, create_session)

    Load a gene_annotation file from MGI

    Parameters
    ----------
      filename : input file name

    References
    ----------
    For the file format see:
    http://www.geneontology.org/GO.format.gaf-1_0.shtml
    http://wiki.geneontology.org/index.php/GAF_2.0
    '''
    session = create_session()
    entries = set()
    for line in file(filename):
        if line[-1] == '\n': line = line[:-1]
        # DO NOT USE
        # line = line.strip()
        #
        # The reason is that there might be empty fields at the end
        # in which case, the line will end with '\t\t\n'. split()
        # handles this case correctly, but strip() would remove the extra
        # tabs.
        if line[0] == '!':
            if line.startswith('!gaf-version:'):
                if not line == '!gaf-version: 2.0':
                    raise IOError("waldo.go.load: Cannot parse. Wrong GAF version.\nHeader line: %s" % line)
            continue
        DB, \
         DB_object_id, \
         DB_object_symbol, \
         qualifier, \
         go_id, \
         db_ref, \
         evidence_code, \
         with_or_from, \
         aspect, \
         DB_object_name, \
         DB_object_synonym, \
         DB_object_type, \
         taxon, \
         date, \
         assigned_by, \
         annotation_cross_products, \
         gene_products = line.split('\t')

        if aspect == 'C':
            if DB_object_id not in entries:
                entry = models.Entry(DB_object_id, DB_object_name)
                entries.add(DB_object_id)
                session.add(entry)
            annotation = models.GOAnnotation(DB_object_id, go_id, assigned_by)
            session.add(annotation)
            session.commit()
