from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

import waldo.nog
import waldo.nog.load
from waldo.nog.load import _accept_species
import waldo.nog.models
from waldo.translations.models import Translation

def test_species():
    assert _accept_species('Mus Musculus', 'ENSMUSP00000083761')
    assert not _accept_species('Mus Musculus', 'ENSP00000247461')
    assert _accept_species('Homo Sapiens', 'ENSP00000247461')
    assert not _accept_species('Homo Sapiens', 'ENSMUSP00000083761')

def test_nog_load():
    engine = create_engine('sqlite://')
    metadata = waldo.nog.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    _testinput = 'tests/data/'

    nr_entries = waldo.nog.load.load(_testinput, sessionmaker_)
    session = sessionmaker_ ()
    loaded = session.query(waldo.nog.models.NogEntry).count()

    assert loaded == nr_entries
    assert loaded == 108
