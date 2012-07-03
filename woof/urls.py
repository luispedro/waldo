import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

print settings._BASE_DIR + '/media'
print 'urls'

urlpatterns = patterns('',
    (r'^search/', include('woof.odlaw.urls')),
    (r'^json/', include('woof.odlaw.urls')),
)
