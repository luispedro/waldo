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
import waldo.hpa.retrieve

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
        hpa_id = waldo.hpa.retrieve.from_ensembl_gene_id(ensemblgene, session)

        uniprot_entry = waldo.uniprot.retrieve.retrieve_entry(uniprot_id, session)
        mgi_entry = waldo.mgi.retrieve.retrieve_entry(mgi_id, session)
        locate_entry = waldo.locate.retrieve.retrieve_entry(locate_id, session)
        esldb_entry = waldo.esldb.retrieve.retrieve_entry(esldb_id, session)
        hpa_entry = waldo.hpa.retrieve.retrieve_entry(hpa_id, session)

        # add each entry to the list
        self.dict['uniprot'] = uniprot_entry and uniprot_entry or None
        self.dict['mgi'] = mgi_entry and mgi_entry or None
        self.dict['locate'] = locate_entry and locate_entry or None
        self.dict['esldb'] = esldb_entry and esldb_entry or None
        self.dict['hpa'] = hpa_entry and hpa_entry or None

    def getBatch(self):
        retval = '%s' % self.id_
        for key in iter(self.dict):
            app = None

            # first, determine if we need an empty set of commas
            if self.dict[key] is None:
                retval += ',None,None'
                continue

            if key is 'uniprot':
                locs = self._processLocations(waldo.uniprot.retrieve.retrieve_go_annotations(self.dict[key].name))
                app = '%s,%s' % (';'.join(locs), 'http://www.uniprot.org/uniprot/%s' % self.dict[key].accessions[0].accession)
            elif key is 'mgi':
                locs = self._processLocations(waldo.mgi.retrieve.retrieve_go_annotations(self.dict[key].mgi_id))
                app = '%s,%s' % (';'.join(locs), 'http://www.informatics.jax.org/searchtool/Search.do?query=%s' % self.dict[key].mgi_id)
            elif key is 'locate':
                locs = self._processLocations(waldo.locate.retrieve.retrieve_go_annotations(self.dict[key].locate_id))
                app = '%s,%s' % (';'.join(locs), 'http://locate.imb.uq.edu.au/cgi-bin/report.cgi?entry=%s' % self.dict[key].locate_id)
            elif key is 'esldb':
                arg = [annot.value for annot in self.dict[key].annotations]
                locs = self._processLocations(arg)
                app = '%s,%s' % (';'.join(locs), 'http://gpcr.biocomp.unibo.it/cgi-bin/predictors/esldb/dettagli.cgi?codice=%s' % self.dict[key].esldb_id)
            elif key is 'hpa':
                locs = waldo.hpa.retrieve.retrieve_location_annotations(self.dict[key].hpa_id)
                app = '%s,%s' % (';'.join([loc[4:] for loc in locs]), 'http://proteinatlas.org/tissue_profile.php?antibody_id=%s' % self.dict[key].hpa_id[-4:])

            retval += ',' + app
        return retval

    def _processLocations(self, locations):
        '''
        The purpose of this function is to remove duplicate entries, as well as
        stripping out unnecessary punctuation.
        
        Input is a list of strings, as is the output.
        '''
        # first, examine if this is an empty list
        if len(locations) == 0:
            return ['Unknown']

        retval = []
        # loop through all the elements of the argument, stripping out punctuation
        # and adding the element to the return list if it has not already
        for location in locations:
            # step 1: if there is any punctuation, split on it
            items = re.split('[,.;:]+', location)
            # for each item, add to the list if it does not already exist
            for item in items:
                item = item.strip() # peel off any trailing or prepended whitespace
                if item not in retval and len(item) > 0: 
                    retval.append(item) 
        return retval

    def getWeb(self):
        pass

