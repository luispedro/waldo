# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

import sys

import waldo.backend
from waldo.groupings import Grouping

session = waldo.backend.create_session()

if len(sys.argv) < 2:
    input = sys.stdin
else:
    input = file(sys.argv[1])

if len(sys.argv) == 3:
    try:
        output = open(sys.argv[2], "w")
    except IOError, e:
        print >>sys.stderr, '''
Error opening '%s': %s

When specifying an output file, please make sure the directory and file is writeable.''' % (sys.argv[2], e)
        sys.exit(1)
else:
    output = sys.stdout


format = "ensemblid,locate_locations,locate_link,mgi_locations,mgi_link,esldb_locations,esldb_link,uniprot_locations,uniprot_link,hpa_locations,hpa_link\n"
output.write(format)
for id in input:
    id = id.strip()
    if not id:
        continue
    ids = Grouping(id.strip(), session)
    output.write(ids.getBatch() + '\n')

if output is not sys.stdout:
    output.close()

