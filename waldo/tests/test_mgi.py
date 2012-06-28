from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

import waldo.mgi
import waldo.mgi.load
import waldo.mgi.models
import waldo.mgi.retrieve
from waldo.translations.models import Translation
from .backend import testdir

def load_mgi_test():
    engine = create_engine('sqlite://')
    metadata = waldo.mgi.models.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)

    nr_entries = waldo.mgi.load.load(testdir, sessionmaker_)
    session = sessionmaker_ ()
    return session, nr_entries

def test_mgi_load():
    session, nr_entries = load_mgi_test()
    loaded = session.query(waldo.mgi.models.Entry).count()

    assert nr_entries == 15
    assert loaded == nr_entries
    # MGI:1915545 is in the file but does not have a cellular component
    assert not session.query(waldo.mgi.models.Entry).filter(waldo.mgi.models.Entry.mgi_id == 'MGI:1915545').count()

    assert 'IEA' in [annot.evidence_code for annot in waldo.mgi.retrieve.retrieve_entry('MGI:1918918', session).go_annotations]

    for namespace in ('mgi:name', 'mgi:id', 'mgi:symbol'):
        assert session.query(Translation).filter(
                            and_(Translation.input_namespace == 'ensembl:gene_id',
                                Translation.input_name == 'ENSMUSG00000026004',
                                Translation.output_namespace == namespace)).count()


def test_mgi():
    session,_ = load_mgi_test()
    def test_annotated(id, go_id, tf):
        first = session.query(waldo.mgi.models.Entry).filter(waldo.mgi.models.Entry.mgi_id == id).first()
        st = go_id in map(lambda ann: ann.go_id, first.go_annotations)
        assert st == tf
    yield test_annotated, 'MGI:1918918', 'GO:0016020', True
    yield test_annotated, 'MGI:1918918', 'GO:0005783', False
    yield test_annotated, 'MGI:1915571', 'GO:0005783', True

