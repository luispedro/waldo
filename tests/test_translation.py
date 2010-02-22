import waldo.translations.models
from nose.tools import raises

def test_verify_namespace_ok():
    waldo.translations.models.verify_namespace('ensembl:gene_id')

@raises(AssertionError)
def test_verify_namespace_fail():
    waldo.translations.models.verify_namespace('ensembl:gene_idasas')

