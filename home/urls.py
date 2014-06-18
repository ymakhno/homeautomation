from django.conf.urls import patterns, include, url

from django.contrib import admin
import lighting

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^', include('lighting.urls'))
    #url(r'^admin/', include(admin.site.urls)),
)
