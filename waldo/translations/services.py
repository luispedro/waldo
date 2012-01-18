# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import waldo.backend
from waldo.translations.models import Translation, verify_namespace
from sqlalchemy import and_
import re

def translate(name, input_namespace, output_namespace, session=None):
    '''
    name = translate(name, input_namespace, output_namespace, session={backend.create_session()})

    Translate from one namespace to another.

    Parameters
    ----------
    name : str
        input name
    input_namespace : str
        namespace to translate from (must be a known namespace)
    output_namespace : str
        namespace to translate to (must be a known namespace)
    session : SQLAlchemy sesion object
        SQLAlchemy session to use (default: call backend.create_session())

    Returns
    -------
    name : str or None
        result of translation or None if not found.
    '''
    if session is None:
        session = waldo.backend.create_session()
    verify_namespace(input_namespace)
    verify_namespace(output_namespace)
    trans = session.query(Translation).filter(
                    and_(Translation.input_namespace == input_namespace,
                    Translation.input_name == name,
                    Translation.output_namespace ==  output_namespace)).first()
    if trans is None:
        if input_namespace == output_namespace:
            return name
        return None
    return trans.output_name

def translate_hops(name, namespaces, session=None):
    '''
    name = translate_hops(name, namespaces, session={backend.create_session()})

    Translate through several namespaces (from namespaces[0] to namespaces[1]
    to namespaces[2] ... namespaces[-1]).

    Parameters
    ----------
    name : str
        input name
    namespaces : list of str
        namespaces to use. First namespace will be the namespace of the
        ``name`` argument.
    session : SQLAlchemy sesion object
        SQLAlchemy session to use (default: call backend.create_session())

    Returns
    -------
    name : str or None
        result of translation or None if not found.
    '''
    while len(namespaces) > 1 and name is not None:
        name = translate(name, namespaces[0], namespaces[1], session)
        namespaces.pop(0)
    return name


def get_id_namespace(any_id):
    # ensembl gene id
    if re.match(r'ENS(\w{3})?G[0-9]+', any_id) is not None:
        return 'ensembl:gene_id'
    # ensembl peptide ID
    if re.match(r'ENS(\w{3})?P[0-9]+', any_id) is not None:
        return 'ensembl:peptide_id'
    # hpa
    if re.match('HPA[0-9]{6}', any_id) is not None:
        return 'hpa:id'
    # mgi
    if re.match('MGI:[0-9]{7}', any_id) is not None:
        return 'mgi:id'
    # uniprot
    if re.match('[0-9A-Z_]{9,11}', any_id) is not None:
        return 'uniprot:name'
    # locate
    if re.match('[0-9]{7}', any_id) is not None:
        return 'locate:id'
    raise ValueError("waldo.translate.get_id_namespace: Unrecognised format for any_id: '%s'" % any_id)
