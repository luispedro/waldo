# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import waldo.backend
from waldo.predictions.models import Prediction

def retrieve_predictions(ensembl_gene_id, session=None):
    '''
    predictions = retrieve_predictions(ensembl_gene_id, session={backend.create_session()})

    Look up predictions by ensembl_gene_id

    Parameters
    ----------
      ensembl_gene_id : Ensembl gene ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      preditions : list of preditions
    '''
    if session is None:
        session = waldo.backend.create_session()
    return session.query(Prediction).filter_by(protein=ensembl_gene_id).all()
