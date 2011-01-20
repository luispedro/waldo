import waldo.sequences.models
import waldo.sequences.load
from tests.backend import create_sessionmaker

def test_load():
    create_session = create_sessionmaker(waldo.sequences.models.Base.metadata)
    nr_loaded = waldo.sequences.load.load('tests/data/', create_session)
    assert nr_loaded == 10

