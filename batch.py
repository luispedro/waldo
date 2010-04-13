# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

import sys

import waldo.backend
from waldo import mgi
from waldo import uniprot
from waldo import esldb
from waldo import locate
from waldo import hpa
from waldo.groupings import Grouping

if len(sys.argv) < 2:
    quit('Please provide a path to a file containing newline-delimited protein IDs.\n' + \
        '\tpython batch.py <inputfile> [outputfile]')

output = None
format = "ensemblid,locate_locations,locate_link,mgi_locations,mgi_link,esldb_locations,esldb_link,uniprot_locations,uniprot_link,hpa_locations,hpa_link"

if len(sys.argv) == 3:
    try:
        output = open(sys.argv[2], "w")
    except IOError:
        quit('When specifying an output file, please make sure the directory and ' + \
            'file is writeable.')

    # print the format for the output
    output.write(format + '\r\n')
else:
    print format
    
session = waldo.backend.create_session()
for id in file(sys.argv[1]):
    if len(id) <= 1: continue
    # process each ID
    ids = Grouping(id.strip(), session)
    if output is None:
        print ids.getBatch()
    else:
        output.write(ids.getBatch() + '\r\n')

if output is not None:
    output.close()
