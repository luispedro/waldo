import waldo.protloc.synergizer
def test_positive():
    key = 'ENSMUSG00000034254'
    trans = waldo.protloc.synergizer.translate_ensembl_gene_to_ensembl_peptide([key])
    assert key in trans
    assert trans[key]

def test_negative():
    key = 'this_is_not_a_key'
    trans = waldo.protloc.synergizer.translate_ensembl_gene_to_ensembl_peptide([key])
    assert key in trans
    assert trans[key] is None

