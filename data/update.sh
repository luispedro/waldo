#!/bin/sh

# MGI
# For some reason, curl does not work with these URLs, but wget does.
wget -N ftp://ftp.informatics.jax.org/pub/reports/go_terms.mgi
wget -N ftp://ftp.informatics.jax.org/pub/reports/go_refs.mgi
wget -N ftp://ftp.informatics.jax.org/pub/reports/gene_association.mgi
wget -N ftp://ftp.informatics.jax.org/pub/reports/MRK_ENSEMBL.rpt
wget -N ftp://ftp.informatics.jax.org/pub/reports/MRK_Reference.rpt

# GO
wget -N http://www.geneontology.org/ontology/obo_format_1_2/gene_ontology.1_2.obo

# Uniprot
wget -N ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz

# LOCATE
wget -N http://locate.imb.uq.edu.au/info_files/LOCATE_mouse_v6_20081121.xml.zip
unzip LOCATE_mouse_v6_20081121.xml.zip
wget -N http://locate.imb.uq.edu.au/info_files/LOCATE_human_v6_20081121.xml.zip
unzip LOCATE_human_v6_20081121.xml.zip

# eSLDB
wget --post-data 'organism=Homo+sapiens&checkbox1_1=SI&checkbox1_2=SI&checkbox1_3=SI&checkbox1_4=SI&checkbox1_5=SI&checkbox1_6=SI&checkbox1_7=SI&checkbox1_8=SI&checkbox1_9=SI&checkbox1_10=SI&f_type=plain' -N -O eSLDB_Homo_sapiens.txt http://gpcr.biocomp.unibo.it/cgi-bin/predictors/esldb/full_download.cgi
wget --post-data 'organism=Mus+musculus&checkbox1_1=SI&checkbox1_2=SI&checkbox1_3=SI&checkbox1_4=SI&checkbox1_5=SI&checkbox1_6=SI&checkbox1_7=SI&checkbox1_8=SI&checkbox1_9=SI&checkbox1_10=SI&f_type=plain' -N -O eSLDB_Mus_musculus.txt http://gpcr.biocomp.unibo.it/cgi-bin/predictors/esldb/full_download.cgi

# This is a FASTA file of mouse protein sequences
wget -N ftp://ftp.ensembl.org/pub/current_fasta/mus_musculus/pep/Mus_musculus.NCBIM37.56.pep.all.fa.gz
