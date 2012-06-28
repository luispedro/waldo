from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

import waldo.hpa
import waldo.hpa.load
import waldo.hpa.models
from waldo.translations.models import Translation
from .backend import testdir

def test_hpa_load():
    engine = create_engine('sqlite://')
    metadata = waldo.hpa.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)

    nr_entries = waldo.hpa.load.load(testdir, sessionmaker_)
    session = sessionmaker_ ()
    loaded = session.query(waldo.hpa.models.Entry).count()

    assert loaded == nr_entries
