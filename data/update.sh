#!/bin/sh

# MGI
# For some reason, curl does not work with these URLs, but wget does.
wget -N ftp://ftp.informatics.jax.org/pub/reports/go_terms.mgi
wget -N ftp://ftp.informatics.jax.org/pub/reports/go_refs.mgi
wget -N ftp://ftp.informatics.jax.org/pub/reports/gene_association.mgi

# GO
wget -N http://www.geneontology.org/ontology/obo_format_1_2/gene_ontology.1_2.obo

