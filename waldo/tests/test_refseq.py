from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import re
import gzip

import waldo.backend
import waldo.translations.models
import waldo.refseq.load
from waldo.translations.services import translate
from .backend import testdir as _testdir

_testfile = _testdir + 'gene2ensembl.gz'

def _load_refseq_test():
    engine = create_engine('sqlite://')
    metadata = waldo.translations.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()

    sessionmaker_ = sessionmaker(engine)
    loaded = waldo.refseq.load.load(_testdir, sessionmaker_)
    session = sessionmaker_()
    return session, loaded

def test_nr_entries():
    nr_entries = len(re.findall('ENSMUSG', gzip.GzipFile(_testfile).read()))
    session,loaded = _load_refseq_test()
    assert loaded == nr_entries
    assert translate('NP_112436', 'refseq:accession','ensembl:gene_id', session) == 'ENSMUSG00000040613'
