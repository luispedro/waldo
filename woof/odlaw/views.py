from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import uniprot.retrieve
import mgi.retrieve
import locatedb.retrieve

def searchby(request):
    if request.method == 'GET':
        ensemblid = request.GET['ensemblid']
        return HttpResponseRedirect('/search/ensemblid/' + ensemblid)

def search(request, ensemblid):
    uniprot_name = uniprot.retrieve.from_ensembl_gene_id(ensemblid)
    uniprot_go_terms = uniprot.retrieve.retrieve_go_annotations(uniprot_name)

    mgi_id = mgi.retrieve.from_ensembl_gene_id(ensemblid)
    mgi_go_terms = mgi.retrieve.retrieve_go_annotations(mgi_id)

    locate_id = locatedb.retrieve.from_ensembl_gene_id(ensemblid)
    locate_go_terms = locatedb.retrieve.retrieve_go_annotations(locate_id)
    return render_to_response(
                'results.html',
                {
                    'genename' : ensemblid,
                    'uniprot_name' : uniprot_name,
                    'uniprot_go_terms' : uniprot_go_terms,
                    'mgi_id' : mgi_id,
                    'mgi_go_terms' : mgi_go_terms,
                    'locate_id' : locate_id,
                    'locate_go_terms' : locate_go_terms,
                })
                 
