from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

import waldo.subcellular
import waldo.subcellular.load
import waldo.subcellular.models
from waldo.translations.models import Translation

def test_subcellular_load():
    engine = create_engine('sqlite://')
    metadata = waldo.subcellular.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    _testinput = 'tests/data/'

    nr_entries = waldo.subcellular.load.load(_testinput, sessionmaker_)
    session = sessionmaker_ ()
    loaded = session.query(waldo.subcellular.models.Entry).count()

    assert loaded == nr_entries
