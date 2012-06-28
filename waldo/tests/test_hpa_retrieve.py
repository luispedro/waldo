from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import waldo.hpa.models
import waldo.hpa.load
import waldo.hpa.retrieve
from waldo.translations.services import translate
from .backend import testdir as _testdir


def test_hpa_retrieve():
    ensembl = 'ENSG00000000003'
    uid = 'HPA000992'

    engine = create_engine('sqlite://')
    metadata = waldo.hpa.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    waldo.hpa.load.load(_testdir, sessionmaker_)
    session = sessionmaker_()
    locations = waldo.hpa.retrieve.retrieve_location_annotations(ensembl, session)
    assert len(locations) == 2

test_hpa_retrieve()
