from django.contrib.syndication.views import Feed
from coltrane.models import Entry, Link

class LatestEntriesFeed(Feed):
    title = "Jason's personal blog entries feeds"
    link = '/feeds/entries/'
    description = "Latest entries in blog"

    def items(self):
        return Entry.objects.order_by('-pub_date')[:5]

    def item_description(self, item):
        return item.body
'''
class CategoryFeed(Feed):
    def get_object(self, request, ):
        pass

    def title(self, obj):
        pass

    def link(self, obj):
        pass

    def description(self, obj):
        pass

    def items(self, obj):
        pass
'''
