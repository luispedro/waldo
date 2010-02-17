from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import waldo.uniprot.retrieve
import waldo.mgi.retrieve
import waldo.locate.retrieve
import waldo.esldb.retrieve
from waldo.translations.services import translate
import waldo.backend

def searchby(request):
    if request.method == 'GET':
        if 'ensemblgene' in request.GET:
            key = 'ensemblgene'
        elif 'ensemblprot' in request.GET:
            key = 'ensemblprot'
        elif 'mgiid' in request.GET:
            key = 'mgiid'
        elif 'protname' in request.GET:
            key = 'protname'
        elif 'uniprotid' in request.GET:
            key = 'uniprotid'
        elif 'locateid' in request.GET:
            key = 'locateid'
        elif 'esldbid' in request.GET:
            key = 'esldbid'
        value = request.GET[key]
        return HttpResponseRedirect('/search/%s/%s' % (key, value))

def search(request, ensemblgene=None, ensemblprot=None, mgiid=None, protname=None, uniprotid=None, locateid=None, esldbid=None):
    if ensemblgene is not None:
        results = _lcd(ensemblgene)
        search_term_type = 'Ensembl gene'
        search_term_value = ensemblgene

    elif ensemblprot is not None:
        results = _lcd(ensemblpeptide=ensemblprot)
        search_term_type = 'Ensembl peptide'
        search_term_value = ensemblprot
    
    elif mgiid is not None:
        results = _lcd(translate(mgiid, 'mgi:id', 'ensembl:gene_id'))
        search_term_type = 'MGI ID'
        search_term_value = mgiid
    
    elif uniprotid is not None:
        results = _lcd(translate(uniprotid, 'uniprot:name', 'ensembl:gene_id'))
        search_term_type = 'Uniprot ID'
        search_term_value = uniprotid
    
    elif locateid is not None:
        results = _lcd(translate(locateid, 'locate:id', 'ensembl:gene_id'))
        search_term_type = 'LOCATE ID'
        search_term_value = locateid
    
    elif protname is not None:
        # FIXME - Implement freetext search
        results = []
        search_term_type = 'Protein name'
        search_term_value = protname

    elif esldbid is not None:
        results = _lcd(ensemblpeptide=translate(esldbid, 'esldb:id', 'ensembl:protein_id'))
        search_term_type = 'eSLDB ID'
        search_term_value = esldbid

    #else: <- free text search
         
    return render_to_response(
                'results.html',
                {
                    'search_term_type' : search_term_type,
                    'search_term_value' : search_term_value,
                    'all_results' : results,
                })

def _lcd(ensemblgene=None, ensemblpeptide=None):
    '''
    list = _lcd(ensemblgene{=None}, ensemblpeptide{=None})

    Returns a formatted list of dictionaries, each pertaining to a result from a
    specific database, in a format that can be outputted as HTML. This function
    behaves as a "least common denominator", using the Ensembl gene or peptide as 
    that identifier by which to find all other information across databases.
    '''
    if ensemblgene is None and ensemblpeptide is None: return None
    session = waldo.backend.create_session()

    # pull out the database-specific IDs
    if ensemblgene is not None:
        uniprot_name = waldo.uniprot.retrieve.from_ensembl_gene_id(ensemblgene, session)
        mgi_id = waldo.mgi.retrieve.from_ensembl_gene_id(ensemblgene, session)
        locate_id = waldo.locate.retrieve.from_ensembl_gene_id(ensemblgene, session)
        esldb_id = waldo.locate.retrieve.from_ensembl_gene_id(ensemblgene, session)
    else:
        uniprot_name = waldo.uniprot.retrieve.from_ensembl_peptide_id(ensemblpeptide, session)
        esldb_id = waldo.esldb.retrieve.from_ensembl_peptide_id(ensemblpeptide, session)
        locate_id = waldo.locate.retrieve.from_ensembl_peptide_id(ensemblpeptide, session)
        mgi_id = waldo.mgi.retrieve.from_ensembl_peptide_id(ensemblpeptide, session)

    # create objects
    uniprot_entry = waldo.uniprot.retrieve.retrieve_entry(uniprot_name, session)
    mgi_entry = waldo.mgi.retrieve.retrieve_entry(mgi_id, session)
    locate_entry = waldo.locate.retrieve.retrieve_entry(locate_id, session)
    esldb_entry = waldo.esldb.retrieve.retrieve_entry(esldb_id, session)

    # for each object, put in correct format
    list = []
    if uniprot_entry is not None:
        dict = {'protein':uniprot_entry.name, 
                'organism': '; '.join([organism.organism for organism in uniprot_entry.organisms]),
                'celltype':'-', 
                'condition':'-', 
                'location': '; '.join(waldo.uniprot.retrieve.retrieve_go_annotations(uniprot_name)), 
                'references': '<br />'.join([paper.title for paper in uniprot_entry.references]), 
                'evidence':'<br />'.join([comment.text for comment in uniprot_entry.comments]), 
                'source':'<a href="http://www.uniprot.org">Uniprot</a>',
                }
        list.append(dict)
    if mgi_entry is not None:
        dict = {'protein': mgi_entry.name,
                'organism':'Mus Musculus',
                'celltype':'-',
                'condition':'-',
                'location':'; '.join(waldo.mgi.retrieve.retrieve_go_annotations(mgi_id)),
                'references':'<br />'.join(['<a href="http://www.ncbi.nlm.nih.gov/pubmed/%s">%s</a>' % (annot.pubmedid, annot.pubmedid) for annot in mgi_entry.annotations]),
                'evidence': '<br />'.join([annot.evidence and annot.evidence or 'None' for annot in mgi_entry.annotations]),
                'source':'<a href="http://www.informatics.jax.org/">MGI</a>',
                }
        list.append(dict)
    if locate_entry is not None:
        dict = {'protein': '%s (%s)' % (locate_entry.accn, locate_entry.source_name),
                'organism': locate_entry.dbtype,
                'celltype': '-',
                'condition': '-',
                'location': '; '.join(waldo.locate.retrieve.retrieve_go_annotations(locate_id)),
                'references':'<br />'.join([ref.title for ref in locate_entry.references]),
                'evidence': '<br />'.join(['<a href="http://locate.imb.uq.edu.au/data_images/%s/%s"><img height="50" width="50" src="http://locate.imb.uq.edu.au/data_images/%s/%s" /></a>' % (img.filename[0:3], img.filename, img.filename[0:3], img.filename) for img in locate_entry.images]),
                'source':'<a href="http://locate.imb.uq.edu.au/">LOCATE</a>',
                }
        list.append(dict)
    if esldb_entry is not None:
        dict = {'protein': esldb_entry.esldb_id,
                'organism': esldb_entry.species,
                'celltype': '-',
                'condition': '-',
                'location': '<br />'.join(['%s: %s' % (annot.type, annot.value) for annot in esldb_entry.annotations]),
                'references': '<br />'.join(['<a href="http://www.uniprot.org/uniprot/%s">%s</a>' % (entry.uniprot_entry, entry.uniprot_entry) for entry in esldb_entry.uniprot_entries]),
                'evidence': '<br />'.join(['<a href="http://www.uniprot.org/uniprot/%s">%s</a>' % (homolog.uniprot_homolog, homolog.uniprot_homolog) for homolog in esldb_entry.uniprot_homologs]),
                'source': '<a href="http://gpcr.biocomp.unibo.it/esldb/">eSLDB</a>',
                }
        list.append(dict)
    return list
