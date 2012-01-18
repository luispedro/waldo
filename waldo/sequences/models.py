# -*- coding: utf-8 -*-
# Copyright (C) 2010, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relation, backref
from waldo.backend import Base

class EnsemblSequence(Base):
    __tablename__ = 'ensembl_sequence'

    seqid = Column(Integer, primary_key=True)
    ensembl_peptide = Column(String(18))
    sequence = Column(Text)

    def __init__(self, ensembl_peptide, sequence):
        self.ensembl_peptide = ensembl_peptide
        self.sequence = sequence

