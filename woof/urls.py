import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

print settings._BASE_DIR + '/media'
print 'urls'

urlpatterns = patterns('',
    (r'^media/(?P<path>.+)$', 'django.views.static.serve', {'document_root': settings._BASE_DIR + '/media'}),
    (r'^search/', include('woof.odlaw.urls')),
    (r'^json/', include('woof.odlaw.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', direct_to_template, {'template' : 'index.html'}, 'home'),
)
