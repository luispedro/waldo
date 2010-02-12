from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import waldo.uniprot.retrieve
import waldo.mgi.retrieve
import waldo.locate.retrieve

def searchby(request):
    if request.method == 'GET':
        ensemblid = request.GET['ensemblid']
        return HttpResponseRedirect('/search/ensemblid/' + ensemblid)

def search(request, ensemblid):
    testing = [{'protein' : 'atf6', 'organism': 'Mus musculus', 'celltype':'?', 
                'condition':'drugged', 'location':'mitochondrial', 'references':'?', 
                'evidence':'?', 'source':'MyDB'}, 
                {'protein':'ABC_123', 'organism':'Homo sapiens', 'celltype':'?', 
                'condition':'ok', 'location':'cytoplasm', 'references':'??',
                'evidence':'????', 'source':'otherDB'}]
    return render_to_response(
                'results2.html',
                {
                    'search_term_type' : 'free text search',
                    'search_term_value' : 'any protein',
                    'all_results' : testing,
                }) 
