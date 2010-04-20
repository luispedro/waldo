Local Database Structure
========================

For every data source (LOCATE, Uniprot, MGI, etc), there were decisions made
regarding what data to extract and store locally and what information was left
in the downloaded files (datasources), possibly for future use. This is an
explanation of the rationale.

eSLDB
-----

eSLDB was used at an earlier stage, but found to contain too much overlap with
uniprot + prediction. We are trying to replicate all of this and, therefore,
eSLDB brought us little extra information.

LOCATE
------

LOCATE contains significant information in its datasources.
Here is a brief list of the information available:

-Protein (organism, name, function, sequence, location)
-Transcript (isoforms)
-Experimental data (images, colocalization images, location)
-External database annotations (locations from external sources)
-Literature evidence (research citations, location)
-Subcellular location predictions (location, method of prediction)
-Motifs (name, position, type, status)
-Memos (memos, methods, scores)
-External References (identifiers into external data sources)
-Topology (methods).

Of these categories, we currently only thoroughly capture information pertaining
to the protein, transcript, external annotations, literature, predictions, and
external references, as these are the only topics that are most directly associated
with subcellular location.

The experimental images, topology, and motifs could be very useful for future work
involving subcellular location prediction.

Uniprot
-------

Currently the information we capture from Uniprot involves accession numbers (which
map directly to Uniprot entries), GO annotations, comments (particularly pertaining
to subcellular location), and direct references. There is a significant amount of 
other information, particularly in the form of external database references
that is not being used (as only those directly referencing Ensembl IDs are currently
used). This could be useful later to cross-reference against other data authorities.

MGI
---

MGI's gene annotations consists of a tab-delimited file where unique entry
identifiers may be repeated throughout the datasource in order to express a
one-to-many relationship with the other values of the additional columns. The
only information from the gene annotations file that is currently used is the
unique MGI identifier, the ensembl ID (cross-referenced from MGI's MRK_Ensembl
file), and the GO location terms.

Much of MGI's data is split up across many different downloadable files, as opposed
to huge single files similar to the other data sources. Literature evidence, for 
example, is also not currently used (as the PubMed IDs for each MGI entry are in
yet a third file), but there are plans to incorporate this information very soon.
