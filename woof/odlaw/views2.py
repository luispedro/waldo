from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import waldo.uniprot.retrieve
import waldo.mgi.retrieve
import waldo.locate.retrieve

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
        testing = [{'protein' : 'atf6', 'organism': 'Mus musculus', 'celltype':'?', 
                'condition':'drugged', 'location':'mitochondrial', 'references':'?', 
                'evidence':'?', 'source':'MyDB'}, 
                {'protein':'ABC_123', 'organism':'Homo sapiens', 'celltype':'?', 
                'condition':'ok', 'location':'cytoplasm', 'references':'??',
                'evidence':'????', 'source':'otherDB'}]
        search_term_type = 'Ensembl gene'
        search_term_value = ensemblgene

    elif ensemblprot is not None:
        search_term_type = 'Ensembl peptide'
        search_term_value = ensemblprot
    
    elif mgiid is not None:
        search_term_type = 'MGI ID'
        search_term_value = mgiid
    
    elif uniprotid is not None:
        search_term_type = 'Uniprot ID'
        search_term_value = uniprotid
    
    elif locateid is not None:
        search_term_type = 'LOCATE ID'
        search_term_value = locateid
    
    elif protname is not None:
        search_term_type = 'Protein name'
        search_term_value = protname

    elif esldbid is not None:
        search_term_type = 'eSLDB ID'
        search_term_value = esldbid

    #else: <- free text search
         
    return render_to_response(
                'results2.html',
                {
                    'search_term_type' : search_term_type,
                    'search_term_value' : search_term_value,
                    'all_results' : 'not yet implemented',
                })
