Waldo Architecture
==================

Each datasource (Uniprot, MGI, LOCATE) has its own independent module, but each
of the datasource modules adheres to a common interface.

Each module should:
-load information from its corresponding flat files into the local relational database
-perform translations from the datasource-specific protein identifiers to the global
ensembl gene IDs, enabling easy searching across all datasources
-be able to retrieve all GO terms corresponding to a given ensembl gene ID / 
datasource-specific identifier

The web front-end can then call these methods for all the available datasources
when a query is issued.

Datasource files are stored in the "data/" folder, and are referenced independently
in each module. As the number of modules grows, this may be redesigned. However,
these are only needed when the data is loaded into the local relational database, 
which should happen very infrequently.

Install & Update
----------------

In order to periodically update the datasources, new versions of the files need
to be pulled down from the servers. Executing the following command will perform
this task::

    ./bin/update-waldo --user --unsafe --verbose

Note: this might take a while, e.g. Uniprot takes about an hour at the time of writing.
