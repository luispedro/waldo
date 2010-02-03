from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import re
import locatedb.models
import locatedb.load
import locatedb.retrieve
from translations.services import translate

_testdir = 'tests/data/'
_testinput1 = _testdir + 'LOCATE_human_SMALL.xml'
_testinput2 = _testdir + 'LOCATE_mouse_SMALL.xml'

def test_retrieve():
    ensembl = 'ENSG00000070785'
    uid = '6000005'

    engine = create_engine('sqlite://')
    metadata = locatedb.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    locatedb.load.load(_testdir, sessionmaker_)
    session = sessionmaker_()
    ret = translate(ensembl, 'ensembl:gene_id', 'locate:id', session)
    assert ret == uid
    ret = locatedb.retrieve.from_ensembl_gene_id(ensembl)
    assert ret == uid
    goids = locatedb.retrieve.retrieve_go_annotations(ret)
    print goids
