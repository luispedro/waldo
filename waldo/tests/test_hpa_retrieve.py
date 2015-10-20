from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import waldo.hpa.models
import waldo.hpa.load
import waldo.hpa.retrieve
from .backend import testdir as _testdir


def test_hpa_retrieve():

    engine = create_engine('sqlite://')
    metadata = waldo.hpa.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    waldo.hpa.load.load(_testdir, sessionmaker_)
    session = sessionmaker_()

    ensembl = 'ENSG00000000003'
    locations = waldo.hpa.retrieve.retrieve_location_annotations(ensembl, session)
    assert locations == ['Cytoplasm']

    ensembl = "ENSG00000002834"
    locations = waldo.hpa.retrieve.retrieve_location_annotations(ensembl, session)
    assert set(locations) == set(["Plasma membrane", "Cytoplasm", "Focal Adhesions"])

