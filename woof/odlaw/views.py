from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def searchby(request):
    if request.method == 'GET':
        ensemblid = request.GET['ensemblid']
        return HttpResponseRedirect('/search/ensemblid/' + ensemblid)

def search(request, ensemblid):
    return render_to_response(
                'results.html',
                {
                    'genename' : ensemblid,
                })
                 
