import backend
import mgi.models

session = backend.create_session()
def test_mgi():
    def test_annotated(id, go_id, tf):
        first = session.query(mgi.models.Entry).filter(mgi.models.Entry.mgi_id == id).first()
        st = go_id in map(lambda ann: ann.go_id, first.annotations)
        assert st == tf
    yield test_annotated, 'MGI:1918918', 'GO:0016020', True
    yield test_annotated, 'MGI:1918918', 'GO:0005783', False
    yield test_annotated, 'MGI:1915571', 'GO:0005783', True

