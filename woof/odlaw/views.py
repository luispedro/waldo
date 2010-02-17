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
    uniprot_name = waldo.uniprot.retrieve.from_ensembl_gene_id(ensemblid)
    uniprot_go_terms = waldo.uniprot.retrieve.retrieve_go_annotations(uniprot_name)

    mgi_id = waldo.mgi.retrieve.from_ensembl_gene_id(ensemblid)
    mgi_go_terms = waldo.mgi.retrieve.retrieve_go_annotations(mgi_id)

    locate_id = waldo.locate.retrieve.from_ensembl_gene_id(ensemblid)
    locate_go_terms = waldo.locate.retrieve.retrieve_go_annotations(locate_id)
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
