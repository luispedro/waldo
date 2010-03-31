# -*- coding: utf-8 -*-
# Copyright (C) 2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

import waldo.backend
import re
from waldo.translations.services import translate
import waldo.uniprot.retrieve
import waldo.mgi.retrieve
import waldo.locate.retrieve
import waldo.esldb.retrieve
#import waldo.hpa.retrieve

class Grouping:

    def __init__(self, id, session=None):
        self.id_ = id
        self.dict = {}

        # which database does it belong to?
        if session is None: session = waldo.backend.create_session()

        ensemblgene = None
        if re.search('ENS(MUS)?G[0-9]+', id) is not None:
            # ensembl gene id
            ensemblgene = id
        elif re.search('ENS(MUS)?P[0-9]+', id) is not None:
            # ensembl peptide ID
            ensemblgene = translate(id, 'ensembl:peptide_id', 'ensembl:gene_id', session)
            pass
        else:
            if re.search('[0-9A-Z_]{9,11}', id) is not None:
                # uniprot
                ensemblgene = translate(id, 'uniprot:name', 'ensembl:gene_id', session)
            elif re.search('MGI:[0-9]{7}', id) is not None:
                # mgi
                ensemblgene = translate(id, 'mgi:id', 'ensembl:gene_id', session)
            elif re.search('(HS|MM)[0-9]{9}', id) is not None:
                # esldb
                ensemblgene = translate(id, 'esldb:id', 'ensembl:gene_id', session)
            elif re.search('[0-9]{7}', id) is not None:
                # locate
                ensemblgene = translate(id, 'locate:id', 'ensembl:gene_id', session)
            elif re.search('HPA[0-9]{6}', id) is not None:
                # hpa
                ensemblgene = translate(id, 'hpa:id', 'ensembl:gene_id', session)
            else:
                quit('ERROR: Unrecognized ID: %s' % id)

        # at this point, we have an ensembl ID...query all the databases
        # with it for any corresponding entries 
        uniprot_id = waldo.uniprot.retrieve.from_ensembl_gene_id(ensemblgene, session)
        mgi_id = waldo.mgi.retrieve.from_ensembl_gene_id(ensemblgene, session)
        locate_id = waldo.locate.retrieve.from_ensembl_gene_id(ensemblgene, session)
        esldb_id = waldo.esldb.retrieve.from_ensembl_gene_id(ensemblgene, session)
        #hpa_id = waldo.hpa.retrieve.from_ensembl_gene_id(ensemblgene, session)

        uniprot_entry = waldo.uniprot.retrieve.retrieve_entry(uniprot_id, session)
        mgi_entry = waldo.mgi.retrieve.retrieve_entry(mgi_id, session)
        locate_entry = waldo.locate.retrieve.retrieve_entry(locate_id, session)
        esldb_entry = waldo.esldb.retrieve.retrieve_entry(esldb_id, session)
        #hpa_entry = waldo.hpa.retrieve.retrieve_entry(hpa_id, session)

        # add each entry to the list
        self.dict['uniprot'] = uniprot_entry and uniprot_entry or None
        self.dict['mgi'] = mgi_entry and mgi_entry or None
        self.dict['locate'] = locate_entry and locate_entry or None
        self.dict['esldb'] = esldb_entry and esldb_entry or None
        #if hpa_entry is not None:
            #self.dict['hpa'] = hpa_entry

    def getBatch(self):
        retval = '%s' % self.id_
        for key in iter(self.dict):
            app = None

            # first, determine if we need an empty set of commas
            if self.dict[key] is None:
                retval += ',None,None'
                continue

            if key is 'uniprot':
                locs = waldo.uniprot.retrieve.retrieve_go_annotations(self.dict[key].name)
                app = '%s,%s' % (len(locs) == 0 and 'Unknown' or ';'.join(locs), 'http://www.uniprot.org/uniprot/%s' % self.dict[key].accessions[0].accession)
            elif key is 'mgi':
                app = '%s,%s' % (';'.join(waldo.mgi.retrieve.retrieve_go_annotations(self.dict[key].mgi_id)), 'http://www.informatics.jax.org/searchtool/Search.do?query=%s' % self.dict[key].mgi_id)
            elif key is 'locate':
                app = '%s,%s' % (';'.join(waldo.locate.retrieve.retrieve_go_annotations(self.dict[key].locate_id)), 'http://locate.imb.uq.edu.au/cgi-bin/report.cgi?entry=%s' % self.dict[key].locate_id)
            elif key is 'esldb':
                app = '%s,%s' % (';'.join([re.split(',|;', annot.value)[0] for annot in self.dict[key].annotations]), 'http://gpcr.biocomp.unibo.it/cgi-bin/predictors/esldb/dettagli.cgi?codice=%s' % self.dict[key].esldb_id)
            elif key is 'hpa':
                # IMPLEMENT ME
                pass

            retval += ',' + app
        return retval

    def getWeb(self):
        pass
