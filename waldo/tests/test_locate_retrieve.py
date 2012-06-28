from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import re
import waldo.locate.models
import waldo.locate.load
import waldo.locate.retrieve
from waldo.translations.services import translate
from .backend import testdir as _testdir

def test_retrieve():
    ensembl = 'ENSG00000070785'
    uid = '6000005'

    engine = create_engine('sqlite://')
    metadata = waldo.locate.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    waldo.locate.load.load(_testdir, sessionmaker_)
    session = sessionmaker_()
    locid = translate(ensembl, 'ensembl:gene_id', 'locate:id', session)
    assert locid == uid
    ret = waldo.locate.retrieve.from_ensembl_gene_id(ensembl, session)
    assert ret == uid
    goids = waldo.locate.retrieve.retrieve_go_annotations(ret, session)

    entry = waldo.locate.retrieve.retrieve_entry(locid, session)
    assert len(entry.organisms) == 1


