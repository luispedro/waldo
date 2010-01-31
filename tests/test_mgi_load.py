from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import mgi
import mgi.load
import mgi.models

def test_mgi_load():
    engine = create_engine('sqlite://')
    metadata = mgi.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    _testinput = 'tests/data/'

    nr_entries = mgi.load.load(_testinput, sessionmaker_)
    session = sessionmaker_ ()
    loaded = session.query(mgi.models.Entry).count()

    assert nr_entries == 15
    assert loaded == nr_entries
    # MGI:1915545 is in the file but does not have a cellular component
    assert not session.query(mgi.models.Entry).filter(mgi.models.Entry.mgi_id == 'MGI:1915545').count()

