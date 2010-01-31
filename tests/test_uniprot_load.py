from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re

import uniprot.load
import uniprot.models

_testinput = 'tests/data/uniprot_small.xml'

def test_nr_entries():
    nr_entries = len(re.findall('</entry>', file(_testinput).read()))

    engine = create_engine('sqlite://')
    metadata = uniprot.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    uniprot.load.load(_testinput, sessionmaker_)
    session = sessionmaker_()
    assert session.query(uniprot.models.Entry).count() == nr_entries

