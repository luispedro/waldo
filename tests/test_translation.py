from waldo.translations.services import get_id_namespace
import waldo.translations.models
from nose.tools import raises

def test_verify_namespace_ok():
    waldo.translations.models.verify_namespace('ensembl:gene_id')

@raises(ValueError)
def test_verify_namespace_fail():
    waldo.translations.models.verify_namespace('ensembl:gene_idasas')

def test_get_id_namespace():
    assert get_id_namespace('ENSGALG00000001190') == 'ensembl:gene_id'
    assert get_id_namespace('ENSGALP00000001190') == 'ensembl:peptide_id'
    assert get_id_namespace('MGI:1918918') == 'mgi:id'
    assert get_id_namespace('2AAA_MOUSE') == 'uniprot:name'
