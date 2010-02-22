# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relation, backref
from waldo.backend import Base

known_namespaces = (
    'ensembl:peptide_id',
    'ensembl:gene_id',
    'ensembl:transcript_id',
    'mgi:id',
    'mgi:symbol',
    'mgi:name',
    'uniprot:name',
    'locate:id',
    'esldb:id',
    )

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
    input_name = Column(String(32))
    output_namespace = Column(String(32))
    output_name = Column(String(32))

    def __init__(self, input_namespace, input_name, output_namespace, output_name):
        '''
        t = Translation(input_namespace, input_name, output_namespace, output_name):

        A translation from input_namespace/input_name to output_namespace/output_name.

        There are no uniqueness guarantees by design.
        '''
        assert input_namespace in known_namespaces, 'waldo.translation: unknown namespace "%s"' % input_namespace
        assert output_namespace in known_namespaces, 'waldo.translation: unknown namespace "%s"' % output_namespace
        self.input_namespace = input_namespace
        self.input_name = input_name
        self.output_namespace = output_namespace
        self.output_name = output_name

    def __repr__(self):
        return '<Translation %s/%s ==> %s/%s>' % (self.input_namespace, self.input_name, self.output_namespace, self.output_name)

