from django.conf.urls.defaults import *
import views
import views2

urlpatterns = patterns('',
    (r'^ensemblgene/(?P<ensemblgene>.*)/?', views2.search),
    (r'^ensemblprot/(?P<ensemblprot>.*)/?', views2.search),
    (r'^mgiid/(?P<mgiid>.*)/?', views2.search),
    (r'^protname/(?P<protname>.*)/?', views2.search),
    (r'^uniprotid/(?P<uniprotid>.*)/?', views2.search),
    (r'^locateid/(?P<locateid>.*)/?', views2.search),
    (r'^esldbid/(?P<esldbid>.*)/?', views2.search),
    (r'^query/?', views2.searchby),
)
