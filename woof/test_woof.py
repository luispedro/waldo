from woof import _retrieve_all
from woof import translate

def test_mgiid():
    mgiid='MGI:1918918'
    assert len(list(_retrieve_all(translate(mgiid, 'mgi:id', 'ensembl:gene_id')))) > 0
