from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import waldo.hpa.models
import waldo.hpa.load
import waldo.hpa.retrieve
from waldo.translations.services import translate

_testdir = 'tests/data/'

def test_hpa_retrieve():
    ensembl = 'ENSG00000066455'
    uid = 'HPA000992'

    engine = create_engine('sqlite://')
    metadata = waldo.hpa.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    waldo.hpa.load.load(_testdir, sessionmaker_)
    session = sessionmaker_()
    hpaid = translate(ensembl, 'ensembl:gene_id', 'hpa:id', session)
    assert hpaid == uid
    ret = waldo.hpa.retrieve.from_ensembl_gene_id(ensembl, session)
    assert ret == uid
    goids = waldo.hpa.retrieve.retrieve_location_annotations(ret, session)
