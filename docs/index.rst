Welcome to Waldo's documentation!
=================================

*Waldo tells what everyone already knows.*

We have a manuscript in preparation. If you use this in a publication, please
let us know so we can (to the best of our knowledge), give you the right
citation.

You can access the waldo webservice at
http://murphylab.web.cmu.edu/services/waldo/home


Example
-------

::
    import waldo.uniprot.retrieve
    from waldo.go import id_to_term

    name = 'ACTB_HUMAN'
    gos = waldo.uniprot.retrieve.retrieve_go_annotations(name)

    for g in gos:
        print id_to_term(g)

This prints out::

    axon
    ortical cytoskeleton
    ytoskeleton
    ytosol
    xtracellular vesicular exosome
    LL5-L complex
    uA4 histone acetyltransferase complex
    ostsynaptic density
    ibonucleoprotein complex

Contents
--------

.. toctree::
   :maxdepth: 2

   install.rst
   tutorial.rst
   identifiers.rst
   architecture.rst
   database.rst
   api.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

