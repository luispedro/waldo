from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import re
import locatedb.load
import locatedb.models
#import locatedb.retrieve
from translations.models import Translation

_testinput = 'tests/data/LOCATE_small.xml'

def test_num_entries():
    num_entries = len(re.findall('</LOCATE_protein>', file(_testinput).read()))

    engine = create_engine('sqlite://')
    metadata = locatedb.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    locatedb.load.load(_testinput, sessionmaker_)
    session = sessionmaker_()
    assert session.query(locatedb.models.Entry).count() = num_entries
    assert session.query(Translation).filter(and_(Translation.input_namespace == 'ensembl:gene_id', Translation.output_namespace == 'locate:id')).count()
