from django.conf.urls.defaults import *

from coltrane.models import Entry

mandatory_entry_info_dict = {
    'queryset': Entry.live.all(),
    'date_field': 'pub_date',
}

optional_dict = {
    'template_object_name': 'object_list',
}

# Change the variable sent to archive_index() to 'object_list' instead of 'latest'
# This is useful for reusing templates because now each will pass the same named object
entry_info_dict = dict(mandatory_entry_info_dict.items() + optional_dict.items())

urlpatterns = patterns('django.views.generic.date_based',
    (r'^$', 'archive_index', entry_info_dict, 'coltrane_entry_archive'),

    (r'^(?P<year>\d{4})/$', 'archive_year', mandatory_entry_info_dict, 'coltrane_entry_archive_year'),

    (r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', mandatory_entry_info_dict, 'coltrane_entry_archive_month'),

    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', mandatory_entry_info_dict, 'coltrane_entry_archive_day'),

    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', mandatory_entry_info_dict, 'coltrane_entry_detail'),
)
