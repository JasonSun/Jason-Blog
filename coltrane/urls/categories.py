from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<slug>[-\w]+)/$', 'coltrane.views.entry_category_detail', {}, 'coltrane_entry_category'),
    (r'^links/(?P<slug>[-\w]+)/$', 'coltrane.views.link_category_detail', {}, 'coltrane_link_category'),
)
