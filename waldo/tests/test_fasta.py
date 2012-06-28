from waldo.sequences import fasta
from waldo.tests.backend import path_to_testfile

def test_read():
    seqs = list(fasta.read(path_to_testfile('test.fasta')))
    assert len(seqs) == 2
    assert seqs[1].header.find('gene:ENSMUSG00000064345')
    assert seqs[1].header[-1] != '\n'
    assert seqs[1].header[0] != '>'

