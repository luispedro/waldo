from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^ensemblgene/(?P<ensemblgene>.*)/?', views.search),
    (r'^ensemblprot/(?P<ensemblprot>.*)/?', views.search),
    (r'^mgiid/(?P<mgiid>.*)/?', views.search),
    (r'^protname/(?P<protname>.*)/?', views.search),
    (r'^uniprotid/(?P<uniprotid>.*)/?', views.search),
    (r'^locateid/(?P<locateid>.*)/?', views.search),
    (r'^esldbid/(?P<esldbid>.*)/?', views.search),
    (r'^query/?', views.searchby),
)
