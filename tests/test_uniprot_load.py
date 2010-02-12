from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import re
import gzip

import waldo.uniprot.load
import waldo.uniprot.models
import waldo.uniprot.retrieve
from waldo.translations.models import Translation

_testdir = 'tests/data/'
_testfile = _testdir + 'uniprot_sprot.xml.gz'

def test_nr_entries():
    nr_entries = len(re.findall('</entry>', gzip.GzipFile(_testfile).read()))

    engine = create_engine('sqlite://')
    metadata = waldo.uniprot.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    waldo.uniprot.load.load(_testdir, sessionmaker_)
    session = sessionmaker_()
    assert session.query(waldo.uniprot.models.Entry).count() == nr_entries
    assert session.query(Translation).filter(and_(Translation.input_namespace == 'ensembl:gene_id', Translation.output_namespace ==  'uniprot:name')).count()
    assert waldo.uniprot.retrieve.from_ensembl_gene_id('ENSMUSG00000007564') == '2AAA_MOUSE'
    assert 'GO:0005829' in waldo.uniprot.retrieve.retrieve_go_annotations('2AAA_MOUSE')
