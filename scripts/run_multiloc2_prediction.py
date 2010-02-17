import os
import waldo.sequences.fasta
import sys

sequences = waldo.sequences.fasta.read('data/Mus_musculus.NCBIM37.56.pep.all.fa.gz')
multiloc_base = sys.argv[1]

genes = set()
for seq in sequences:
    genename = seq.header[seq.header.find('gene:')+len('gene:'):].split()[0]
    if genename in genes:
        continue
    genes.add(genename)
    fastat = file('FILE.fasta', 'w')
    print >>fastat, '>%s' % genename
    sequence = seq.sequence 
    while sequence:
        print >>fastat, sequence[:72]
        sequence = sequence[72:]
    fastat.close()
    os.system("python %ssrc/multiloc2_prediction.py -fasta=FILE.fasta -origin=animal -result=output.txt" % multiloc_base)
    os.system("cat output.txt >> data/accumulate.txt")
