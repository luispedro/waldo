#!/bin/sh

# MGI
# For some reason, curl does not work with these URLs, but wget does.
wget -N ftp://ftp.informatics.jax.org/pub/reports/go_terms.mgi
wget -N ftp://ftp.informatics.jax.org/pub/reports/go_refs.mgi
wget -N ftp://ftp.informatics.jax.org/pub/reports/gene_association.mgi
wget -N ftp://ftp.informatics.jax.org/pub/reports/MRK_ENSEMBL.rpt

# GO
wget -N http://www.geneontology.org/ontology/obo_format_1_2/gene_ontology.1_2.obo

# Uniprot
wget -N ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz

# LOCATE
wget -N http://locate.imb.uq.edu.au/info_files/
wget -N http://locate.imb.uq.edu.au/info_files/

# eSLDB
# POST to /cgi-bin/predictors/esldb/full_download.cgi
