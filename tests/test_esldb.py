import protloc.esldb
def test_esldb():
    res = protloc.esldb.locate(ensembl='ENSMUSG00000034254')
    assert res
