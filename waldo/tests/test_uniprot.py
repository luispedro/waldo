import waldo.uniprot

def test_retrieve_go_annotation():
    # This is a regression
    waldo.uniprot.retrieve_go_annotations('1A43_HUMAN')

