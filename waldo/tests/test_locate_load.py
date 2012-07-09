from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import re
import waldo.locate.models
import waldo.locate.load
import waldo.locate.retrieve
from waldo.translations.models import Translation
from .backend import testdir as _testdir

_testinput1 = _testdir + 'LOCATE_human_v6_20081121.xml.zip'
_testinput2 = _testdir + 'LOCATE_mouse_v6_20081121.xml.zip'

def read_zipfile(fname):
    import zipfile
    zf = zipfile.ZipFile(fname)
    return zf.open(zf.filelist[0])

def test_num_entries():
    num_entries = len(re.findall('</LOCATE_protein>', read_zipfile(_testinput1).read()))
    num_entries += len(re.findall('</LOCATE_protein>', read_zipfile(_testinput2).read()))

    engine = create_engine('sqlite://')
    metadata = waldo.locate.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    waldo.locate.load.load(_testdir, sessionmaker_)
    session = sessionmaker_()
    assert session.query(waldo.locate.models.Entry).count() == num_entries
    assert session.query(Translation).filter(and_(Translation.input_namespace == 'ensembl:gene_id', Translation.output_namespace == 'locate:id')).count()

    e = session.query(waldo.locate.models.Entry).get('6000072')
    assert e.name == 'cyclin-dependent kinase 9'


    waldo.locate.load.clear(sessionmaker_)
    assert session.query(waldo.locate.models.Entry).count() == 0
