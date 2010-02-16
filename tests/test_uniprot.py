import waldo.uniprot.online
def test_uniprot():
    res = waldo.uniprot.online.query(ensembl='ENSMUSG00000034254')
    assert res
