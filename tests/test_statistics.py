from waldo import statistics
from test_uniprot_load import load_uniprot_test

#def test_locate_statistics():
#    statistics.locatestats()

def test_uniprot_statistics():
    session,_ = load_uniprot_test()
    statistics.uniprotstats(session)

#def test_mgi_statistics():
#    statistics.mgistats()
