from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^ensemblid/(?P<ensemblid>.*)/?', views.search),
    (r'^query/?', views.searchby),
)

