======================
Identifier Translation
======================

One of waldo's features is the ability to translate between different gene
identifiers.

It knows about the following identifier types:

- ``embl:cds`` *EMBL CDS*
- ``ensembl:peptide_id`` *ENSEMBL Peptide ID*
- ``ensembl:gene_id`` *ENSEMBL Gene ID*
- ``ensembl:transcript_id`` *ENSEMBL Transcript ID*
- ``mgi:id`` *MGI ID*
- ``mgi:symbol`` *MGI Symbol*
- ``mgi:name`` *MGI Name*
- ``refseq:accession`` *RefSeq Accession*
- ``uniprot:name`` *Uniprot Name*
- ``uniprot:accession`` *Uniprot Accession*
- ``locate:id`` *Locate ID*
- ``hpa:id`` *Human Protein Atlas ID*

The strings like ``ensembl:gene_id`` are the ones used in the code.

Here is a simple example of how to translate Uniprot accessions to Uniprot
names::

    from waldo import translate
    accessions = [
        'P60709',
        'P07437',
        'Q9BQE3',
        'Q9NY65',
    ]
    for a in accessions:
        n = translate(a, 'uniprot:accession', 'uniprot:name')
        print('{} -> {}'.format(a, n))

Prints out::

    P60709 -> ACTB_HUMAN
    P07437 -> TBB5_HUMAN
    Q9BQE3 -> TBA1C_HUMAN
    Q9NY65 -> TBA8_HUMAN

