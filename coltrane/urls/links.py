from django.conf.urls.defaults import *

from coltrane.models import Link

link_info_dict = {
    'queryset': Link.objects.all(),
    'date_field': 'pub_date',
}

explicit_name_dict = {
    'template_object_name': 'object_list',
}

# Change the variable sent to archive index to 'object_list' instead of 'latest'
# This is useful for reusing templates because now each will pass the same named object
explicit_link_info_dict = dict(link_info_dict.items() + explicit_name_dict.items())

urlpatterns = patterns('django.views.generic.date_based',
    (r'^$', 'archive_index', explicit_link_info_dict, 'coltrane_link_archive_index'),
    
    (r'^(?P<year>\d{4})/$', 'archive_year', link_info_dict, 'coltrane_link_archive_year'),
    
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', link_info_dict, 'coltrane_link_archive_month'),
    
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', link_info_dict, 'coltrane_link_archive_day'),
    
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', link_info_dict, 'coltrane_link_detail'),

)
