from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import waldo.uniprot.retrieve
import waldo.mgi.retrieve
import waldo.locate.retrieve
import waldo.esldb.retrieve
from waldo.translation.services import translate

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
        results = _lcd(translate(esldbid, 'esldb:id', 'ensembl:gene_id'))
        search_term_type = 'eSLDB ID'
        search_term_value = esldbid

    #else: <- free text search
         
    return render_to_response(
                'results2.html',
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

    # pull out the database-specific IDs
    if ensemblgene is not None:
        uniprot_name = waldo.uniprot.retrieve.from_ensembl_gene_id(ensemblgene)
        mgi_id = waldo.mgi.retrieve.from_ensembl_gene_id(ensemblgene)
        locate_id = waldo.locate.retrieve.from_ensembl_gene_id(ensemblgene)
        esldb_id = waldo.locate.retrieve.from_ensembl_gene_id(ensemblgene)
    else:
        uniprot_name = waldo.uniprot.retrieve.from_ensembl_peptide_id(ensemblpeptide)
        esldb_id = waldo.esldb.retrieve.from_ensembl_peptide_id(ensemblpeptide)
        locate_id = waldo.locate.retrieve.from_ensembl_peptide_id(ensemblpeptide)
        mgi_id = waldo.mgi.retrieve.from_ensembl_peptide_id(ensemblpeptide)

    # create objects
    uniprot_entry = waldo.uniprot.retrieve.retrieve_entry(uniprot_name)
    mgi_entry = waldo.mgi.retrieve.retrieve_entry(mgi_id)
    locate_entry = waldo.locate.retrieve.retrieve_entry(locate_id)
    esldb_entry = waldo.locate.retrieve.retrieve_entry(esldb_id)

    # for each object, put in correct format

    list = []
    list = [{'protein' : 'something', 'organism': 'Mus musculus', 'celltype':'?', 
                'condition':'drugged', 'location':'mitochondrial', 'references':'?', 
                'evidence':'?', 'source':'MyDB'}, 
                {'protein':'ABC_123', 'organism':'Homo sapiens', 'celltype':'?', 
                'condition':'ok', 'location':'cytoplasm', 'references':'??',
                'evidence':'????', 'source':'otherDB'}]
    return list
