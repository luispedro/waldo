Database Querying API
=====================

Uniprot.retrieve
----------------

To translate Ensembl Ids into Uniprot names, two methods are provided:
    - From Ensembl gene id:
        uniprot_name = from_ensembl_gene_id(ensembl_gene_id, sqlalchemy_session)
    - From Ensembl peptide id:
        uniprot_peptide_name = from_ensembl_peptide_id(ensemble_peptide_id, sqlalchemy_session)

To retrieve a list of GO Id strings (of the form "GO:00...") using the Uniprot name:
        go_ids = retrieve_go_annotations(name, sqlalchemy_session)

To retrieve a Uniprot database entry using the Uniprot name:
        entry = retrieve_entry(name, sqlalchemy_session)
    
    A Uniprot entry contains the human readable protein name, GO Annotations,
    organisms, accessions, references, comments, and the protein's sequence. 

Go Annotations are often accompanied by two to three letter evidence codes, to
determine the meaning of an evidence code, a method is provided to convert the 
evidence codes given in entry.go_annotations.evidence_code to a convenient
description.
        description = translate_evidence_code(evidence_code)


To retrieve a paper's abstract given its PubMed id or DOI code, two methods are 
provided:
        - For PubMed Ids :
            abstract = retrieve_pubmed_abstract(pubmed_id)
        - For DOI codes :
            abstract = retrieve_doi_abstract(doi_code)

        Note that retrieve_doi_abstract simply looks up the PubMed Id associated
        with the DOI code, and so will fail if the paper does not have one.

Additionally, retrieve_name_matches is provided to find Uniprot entries by 
searching a term and finding Uniprot names that contain the term or similar terms.
        entries = retrieve_name_matches(term, sqlalchemy_session)

