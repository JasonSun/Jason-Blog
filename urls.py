from django.conf.urls.defaults import *
from django.contrib import admin
import settings # Needed for MEDIA_ROOT
from coltrane.feeds import LatestEntriesFeed

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),

    #Static media url not needed for production because it is being served by nginx
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

    (r'^about/$', 'django.views.generic.simple.direct_to_template', {'template': 'about.html'}),
    (r'^categories/', include('coltrane.urls.categories')),
    (r'^links/', include('coltrane.urls.links')),
    (r'^tags/', include('coltrane.urls.tags')),
    (r'^blog/', include('coltrane.urls.entries')),
    (r'^feeds/entries/$', LatestEntriesFeed()),
)
