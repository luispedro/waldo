from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

import waldo.esldb
import waldo.esldb.load
import waldo.esldb.models
from waldo.translations.models import Translation

def test_esldb_load():
    engine = create_engine('sqlite://')
    metadata = waldo.esldb.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    _testinput = 'tests/data/'

    nr_entries = waldo.esldb.load.load(_testinput, sessionmaker_)
    session = sessionmaker_ ()
    loaded = session.query(waldo.esldb.models.Entry).count()

    assert loaded == nr_entries
