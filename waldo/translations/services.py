# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import waldo.backend
from waldo.translations.models import Translation
from sqlalchemy import and_

def translate(name, input_namespace, output_namespace, session=None):
    '''
    name = translate(name, input_namespace, output_namespace, session={backend.create_session()})

    Translate from one namespace to another.

    Parameters
    ----------
      name : input name
      input_namespace : namespace to translate from
      output_namespace : namespace to translate to
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      name : result of translation or None.
    '''
    if session is None:
        session = waldo.backend.create_session()
    trans = session.query(Translation).filter(
                    and_(Translation.input_namespace == input_namespace,
                    Translation.input_name == name,
                    Translation.output_namespace ==  output_namespace)).first()
    if trans is None:
        return None
    return trans.output_name
