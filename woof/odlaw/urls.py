from django.conf.urls.defaults import *
import views
import views2

urlpatterns = patterns('',
    (r'^ensemblid/(?P<ensemblid>.*)/?', views2.search),
    (r'^query/?', views2.searchby),
)

