# -*- coding: utf-8 -*-
# Copyright (C) 2009-2013, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relation, backref
from waldo.backend import Base

namespace_fullname = {
    'embl:cds': 'EMBL CDS',
    'ensembl:peptide_id' : 'ENSEMBL Peptide ID',
    'ensembl:gene_id': 'ENSEMBL Gene ID',
    'ensembl:transcript_id' : 'ENSEMBL Transcript ID',
    'mgi:id' : 'MGI ID',
    'mgi:symbol': 'MGI Symbol',
    'mgi:name': 'MGI Name',
    'refseq:accession': 'RefSeq Accession',
    'uniprot:name': 'Uniprot Name',
    'uniprot:accession': 'Uniprot Accession',
    'locate:id': 'Locate ID',
    'hpa:id': 'Human Protein Atlas ID',
    }
known_namespaces = tuple(namespace_fullname.keys())

def verify_namespace(namespace):
    '''
    verify_namespace(namespace)

    Checks whether namespace is known.
    Raises an exception if it not.

    Parameters
    ----------
    namespace : str
        Possible namespace

    Raises
    ------
    ValueError

    Returns
    -------
    None
    '''
    if namespace not in known_namespaces:
        raise ValueError('waldo.translation: unknown namespace "%s"' % namespace)

class Translation(Base):
    '''
    Logically, a two-column table:
        input -> output

    but the each column is broken up into
        (namespace, name)

    so it becomes a four column table.
    '''
    __tablename__ = 'translation'

    trans_id = Column(Integer, primary_key=True)
    input_namespace = Column(String(32))
    input_name = Column(String(32), index=True)
    output_namespace = Column(String(32))
    output_name = Column(String(32))

    def __init__(self, input_namespace, input_name, output_namespace, output_name):
        '''
        t = Translation(input_namespace, input_name, output_namespace, output_name):

        A translation from input_namespace/input_name to output_namespace/output_name.

        There are no uniqueness guarantees by design.
        '''
        verify_namespace(input_namespace)
        verify_namespace(output_namespace)
        self.input_namespace = input_namespace
        self.input_name = input_name
        self.output_namespace = output_namespace
        self.output_name = output_name

    def __repr__(self):
        return '<Translation %s/%s ==> %s/%s>' % (self.input_namespace, self.input_name, self.output_namespace, self.output_name)

translation_index = sqlalchemy.Index('translation_index',
        Translation.input_namespace,
        Translation.input_name,
        Translation.output_namespace,
        )

