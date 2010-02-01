from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import uniprot.retrieve

def searchby(request):
    if request.method == 'GET':
        ensemblid = request.GET['ensemblid']
        return HttpResponseRedirect('/search/ensemblid/' + ensemblid)

def search(request, ensemblid):
    uniprot_name = uniprot.retrieve.from_ensembl_gene_id(ensemblid)
    go_terms = uniprot.retrieve.retrieve_go_annotations(uniprot_name)
    return render_to_response(
                'results.html',
                {
                    'genename' : ensemblid,
                    'uniprot_name' : uniprot_name,
                    'uniprot_goterms' : go_terms,
                })
                 
