import waldo.protloc.uniprot
def test_uniprot():
    res = waldo.protloc.uniprot.locate(ensembl='ENSMUSG00000034254')
    assert res
