from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import re
import locatedb.models
import locatedb.load
import locatedb.retrieve
from translations.models import Translation

_testdir = 'tests/data/'
_testinput1 = _testdir + 'LOCATE_human.xml'
_testinput2 = _testdir + 'LOCATE_mouse.xml'

def test_num_entries():
    num_entries = len(re.findall('</LOCATE_protein>', file(_testinput1).read()))
    num_entries += len(re.findall('</LOCATE_protein>', file(_testinput2).read()))

    engine = create_engine('mysql://djangouser@localhost/django')
    metadata = locatedb.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    locatedb.load.load(_testdir, sessionmaker_)
    session = sessionmaker_()
    assert session.query(locatedb.models.Entry).count() == num_entries
    assert session.query(Translation).filter(and_(Translation.input_namespace == 'ensembl:gene_id', Translation.output_namespace == 'locate:id')).count()
