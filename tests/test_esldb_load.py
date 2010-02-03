from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

import esldb
import esldb.load
import esldb.models
from translations.models import Translation

def test_esldb_load():
    engine = create_engine('sqlite://')
    metadata = esldb.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    _testinput = 'tests/data/'

    nr_entries = esldb.load.load(_testinput, sessionmaker_)
    session = sessionmaker_ ()
    loaded = session.query(esldb.models.Entry).count()

    assert loaded == nr_entries
