#!/bin/sh

# MGI
# For some reason, curl does not work with these URLs, but wget does.
wget -N ftp://ftp.informatics.jax.org/pub/reports/go_terms.mgi
wget -N ftp://ftp.informatics.jax.org/pub/reports/go_refs.mgi
wget -N ftp://ftp.informatics.jax.org/pub/reports/gene_association.mgi
wget -N ftp://ftp.informatics.jax.org/pub/reports/MRK_ENSEMBL.rpt
wget -N ftp://ftp.informatics.jax.org/pub/reports/MRK_Reference.rpt

# MGI GO SLIM
wget -N http://www.informatics.jax.org/gotools/data/input/map2MGIslim.txt

# GO
wget -N http://www.geneontology.org/ontology/obo_format_1_2/gene_ontology.1_2.obo

# Uniprot
wget -N ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz

# LOCATE
wget -N http://locate.imb.uq.edu.au/info_files/LOCATE_mouse_v6_20081121.xml.zip
unzip -u LOCATE_mouse_v6_20081121.xml.zip
wget -N http://locate.imb.uq.edu.au/info_files/LOCATE_human_v6_20081121.xml.zip
unzip -u LOCATE_human_v6_20081121.xml.zip

# This is a FASTA file of mouse protein sequences
wget -N ftp://ftp.ensembl.org/pub/current/fasta/mus_musculus/pep/Mus_musculus.NCBIM37.*.pep.all.fa.gz

# HPA
wget -N http://www.proteinatlas.org/download/subcellular_location.csv.zip
unzip -u subcellular_location.csv.zip
