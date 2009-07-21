import protloc.uniprot
def test_uniprot():
    res = protloc.uniprot.locate(ensembl='ENSMUSG00000034254')
    assert res
