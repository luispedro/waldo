import waldo.sequences.models
import waldo.sequences.load
from waldo.sequences.retrieve import peptide_sequence
from waldo.tests.backend import create_sessionmaker, testdir

def test_load():
    create_session = create_sessionmaker(waldo.sequences.models.Base.metadata)
    nr_loaded = waldo.sequences.load.load(testdir, create_session)
    assert nr_loaded == 10

    assert peptide_sequence('ENSMUSP00000089350', create_session) is not None
    assert peptide_sequence('ENSMUSP00000089350', create_session).startswith('MPEPAKSAPAPKKGSKKAVTKAQKKDGKKRKRSRKESYSVYVYKVLKQVHPDTGISSKAM')
    assert peptide_sequence('ENSMUSP00000089350', create_session) != peptide_sequence('ENSMUSP00000053565', create_session)

