# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from waldo.backend import Base

class Prediction(Base):
    '''
    Prediction table

    General prediction table.

    Fields
    ------
    - predictor : origin of prediction
    - protein : protein
    - prediction : prediction
    - strength : strength of prediction

    The `strength` is in the units reported by the predictor.
    If the predictor does not report strength, then this field should be NULL.
    '''
    __tablename__ = 'prediction'
    
    pid = Column(Integer, primary_key=True)
    protein = Column(String(64))
    predictor = Column(String(64))
    prediction = Column(String(32))
    strength = Column(Float)

    def __init__(self, predictor, protein, prediction, strength=None):
        assert strength is None or float(strength) == strength, \
            'waldo.prediction.Prediction: strength argument does not seem to be of the right type.'
        self.predictor = predictor
        self.protein = protein
        self.prediction = prediction
        self. strength = strength

