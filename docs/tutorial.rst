==============
Waldo Tutorial
==============

We assume you have already installed waldo and its databases. We will show you
how to use it as a library.

Our task will be to find out more information about 3 mouse proteins, listed
using MGI (Mouse Genome Informatics) gene IDs:

1. `Actn1 <http://www.informatics.jax.org/marker/MGI:2137706>`__
2. `Cdc42 <http://www.informatics.jax.org/marker/MGI:106211>`__
3. `Fah <http://www.informatics.jax.org/marker/MGI:95482>`__

If we want to look up the GO locations within MGI, we could simply do::


    import waldo.mgi
    annotations = waldo.mgi.retrieve_go_annotations('Actn1')
    print annotations

Prints out::

    [u'GO:0000139',
     u'GO:0005622',
     u'GO:0005622',
     u'GO:0005623',
     u'GO:0005737',
     u'GO:0005737',
     u'GO:0005737',
     u'GO:0005856',
     u'GO:0005886',
     u'GO:0005886',
     u'GO:0016020',
     u'GO:0030141',
     u'GO:0030175',
     u'GO:0030496',
     u'GO:0042995',
     u'GO:0043005',
     u'GO:0043025',
     u'GO:0045177',
     u'GO:0051233',
     u'GO:0071944',
     u'GO:0072686']

These are Gene Ontology IDs, but they are hard to understand, we can get the
English version with ``waldo.go.id_to_term``::

    from waldo.go import id_to_term
    print map(id_to_term, annotations)

Now, you see::

    [u'Golgi membrane',
     u'intracellular',
     u'intracellular',
     u'cell',
     u'cytoplasm',
     u'cytoplasm',
     u'cytoplasm',
     u'cytoskeleton',
     u'plasma membrane',
     u'plasma membrane',
     u'membrane',
     u'secretory granule',
     u'filopodium',
     u'midbody',
     u'cell projection',
     u'neuron projection',
     u'neuronal cell body',
     u'apical part of cell',
     u'spindle midzone',
     u'cell periphery',
     u'mitotic spindle']


To get information on all the genes we had above, we can now just use standard
Python constructs::

    genes = ['Actn1', 'Cdc42', 'Fah']
    annotations = {}
    for g in genes:
        annotations[g] = waldo.mgi.retrieve_go_annotations(g)

Other Databases
---------------

First we need to deal with **identifiers**.  Proteins can be identified in many
ways. Mapping identifiers is itself often a big problem.

Waldo uses **ENSEMBL identifiers** as the common identifiers. It knows how to
convert identifiers from the other databases to Ensembl and back. Above, we
listed MGI symbols, so they worked with MGI look up. Now, we will convert them
to see what `Uniprot <http://www.uniprot.org/>`__ has to say.

First, we get the ensembl gene ID::

    from waldo import translate
    for g in genes:
        print translate(g, 'mgi:symbol', 'ensembl:gene_id')

This prints out (see the `identifier section <identifiers.html>`__ to learn
about the identifiers that Waldo knows about)::

    ENSMUSG00000015143
    ENSMUSG00000006699
    ENSMUSG00000030630

To get a uniprot name, we need two steps::

    for g in genes:
        e = translate(g, 'mgi:symbol', 'ensembl:gene_id')
        uname = translate(e, 'ensembl:gene_id', 'uniprot:name')
        print uname

To get::

    ACTN1_MOUSE
    CDC42_MOUSE
    FAAA_MOUSE

We now just look these up using the Uniprot module::

    import waldo.uniprot

    for g in genes:
        e = translate(g, 'mgi:symbol', 'ensembl:gene_id')
        uname = translate(e, 'ensembl:gene_id', 'uniprot:name')
        print waldo.uniprot.retrieve_go_annotations(uname)

Voilà!

