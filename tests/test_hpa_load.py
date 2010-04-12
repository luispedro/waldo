from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

import waldo.hpa
import waldo.hpa.load
import waldo.hpa.models
from waldo.translations.models import Translation

def test_esldb_load():
    engine = create_engine('sqlite://')
    metadata = waldo.hpa.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    _testinput = 'tests/data/'

    nr_entries = waldo.hpa.load.load(_testinput, sessionmaker_)
    session = sessionmaker_ ()
    loaded = session.query(waldo.hpa.models.Entry).count()

    assert loaded == nr_entries
