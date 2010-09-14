# -*- coding: utf-8 -*-
# Copyright (C) 2010, Shannon Quinn <squinn@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

import re

from waldo.translations.services import translate, get_id_namespace
import waldo.uniprot.retrieve
import waldo.mgi.retrieve
import waldo.locate.retrieve
import waldo.hpa.retrieve
import waldo.backend


def get_information(protein_id, session=None):
    '''
    information = get_information(protein_id, session={backend.create_session()})

    Returns all information on the protein identified by `protein_id`

    Parameters
    ----------
    protein_id : string
            protein ID in one of the formats accepted by Waldo
    session : database connection, optional
            database connection to use

    Returns
    -------
    information : string
            CSV representation of all information on `protein_id`
    '''

    def get_data(module):
        spec_id = module.from_ensembl_gene_id(ensemblgene, session)
        if not spec_id:
            return 'None, None'
        locs = module.retrieve_go_annotations(spec_id)
        all_locs = []
        for ls in locs:
            all_locs.extend([loc.strip() for loc in re.split('[,.;:]+', ls)])
        all_locs = list(set(all_locs))
        all_locs = ';'.join(all_locs)
        url = module.gen_url(spec_id)
        return '%s,%s' % (all_locs, url)

    if session is None:
        session = waldo.backend.create_session()
    ensemblgene = translate(protein_id, get_id_namespace(protein_id), 'ensembl:gene_id', session) 

    return ','.join([
        ensemblgene,
        get_data(waldo.uniprot.retrieve),
        get_data(waldo.mgi.retrieve),
        get_data(waldo.locate.retrieve),
        get_data(waldo.hpa.retrieve),
        ])


