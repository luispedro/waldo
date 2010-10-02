from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

import waldo.goslim.goslim
import waldo.goslim.load
import waldo.goslim.models

def test_load():
    engine = create_engine('sqlite://')
    metadata = waldo.goslim.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    _testinput = 'tests/data/'

    sessionmaker_ = sessionmaker(engine)
    nr_entries, nr_aspects = waldo.goslim.load.load(_testinput, sessionmaker_)
    inputfile = open(_testinput + waldo.goslim.load._inputfilename)
    nr_lines = len(inputfile.readlines())
    assert nr_entries == (nr_lines-1)
    aspects = set()
    inputfile = open(_testinput + waldo.goslim.load._inputfilename)
    lines = inputfile.readlines()
    for line in lines[1:]:
        tokens = line.strip().split('\t')
        aspects.add(tokens[-2])
    assert len(aspects) == nr_aspects
    session = sessionmaker_()
    name = waldo.goslim.goslim.map_to_goslim('GO:0014709', 'mgi', session)
    assert name == 'developmental processes'
