from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^ensemblgene/(?P<ensemblgene>.*)/?', views.search),
    (r'^ensemblprot/(?P<ensemblprot>.*)/?', views.search),
    (r'^mgiid/(?P<mgiid>.*)/?', views.search),
    (r'^protname/(?P<protname>.*)/?', views.search),
    (r'^uniprotid/(?P<uniprotid>.*)/?', views.search),
    (r'^locateid/(?P<locateid>.*)/?', views.search),
    (r'^query/?', views.searchby),
    (r'^location/(?P<id>.*)/?', views.get_json),
    (r'^uniprot/(?P<id>.*)/?', views.get_json),
    (r'^sequences/(?P<id>.*)/?', views.get_json),
    (r'^nog/(?P<id>.*)/?', views.get_json),
    (r'^prediction/(?P<id>.*)/?', views.get_json),
    (r'^mgi/(?P<id>.*)/?', views.get_json),
)
