import waldo.uniprot.retrieve
import waldo.mgi.retrieve
import waldo.locate.retrieve
import waldo.hpa.retrieve
def test_gen_url():
    assert waldo.uniprot.retrieve.gen_url('ATF6_HUMAN').startswith('http://')
    assert waldo.mgi.retrieve.gen_url('MGI:1918918').startswith('http://')
    assert waldo.mgi.retrieve.gen_url('MGI:1918918').startswith('http://')
    assert waldo.locate.retrieve.gen_url('1918918').startswith('http://')

