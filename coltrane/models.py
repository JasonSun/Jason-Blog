import datetime

from django.contrib.auth.models import User
from django.db import models

from markdown import markdown
from wmd import models as wmd_models
import tagging
from tagging.fields import TagField

class Category(models.Model):
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text="Suggested value automatically generated from title. Must be unique.")
    description = models.TextField()

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title

    def live_entry_set(self):
        from coltrane.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)

    def get_link_set(self):
        from coltrane.models import Link
        return self.link_set.all()

    def count_for_model(self, model):
        """Returns the number of objects of a certain model that use this category"""
        manager = model._default_manager
        return manager.filter(categories=self).count()

    @models.permalink
    def get_absolute_entries_url(self):
        return ('coltrane_entry_category', (), { 'slug': self.slug })

    @models.permalink
    def get_absolute_links_url(self):
        return ('coltrane_link_category', (), { 'slug': self.slug })

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique_for_date='pub_date')
    body = wmd_models.MarkDownField(verbose_name = 'Content')
    body_html = wmd_models.MarkDownField(editable = False, blank = True)
    pub_date = models.DateTimeField(default=datetime.datetime.now, verbose_name = 'Date Published')
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    categories = models.ManyToManyField(Category)
    tags = TagField()

    # Need to be this way around so that non-live entries will show up in Admin, which uses the default (first) manager.
    live = LiveEntryManager()
    objects = models.Manager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = "Entries"

    def __unicode__(self):
        return self.title

    def save(self, force_insert = False, force_update = False):
        self.body_html = markdown(self.body)
        super(Entry, self).save(force_insert, force_update)

    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_entry_detail', (), {  'year': self.pub_date.strftime("%Y"),
                                                'month': self.pub_date.strftime("%b").lower(),
                                                'day': self.pub_date.strftime("%d"),
                                                'slug': self.slug })

# See http://blog.sveri.de/index.php?/categories/2-Django
try:
    tagging.register(Entry, tag_descriptor_attr='etags')
except tagging.AlreadyRegistered:
    pass

class Link(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique_for_date='pub_date', help_text='Must be unique for the publication date.')
    url = models.URLField(unique=True)
    description = wmd_models.MarkDownField()
    description_html = wmd_models.MarkDownField(editable = False, blank = True)
    via_name = models.CharField(max_length=250, blank=True, help_text='The name of the person whose site you spotted the link on. Optional.')
    via_url = models.URLField(blank=True, help_text='The URL of the site where you spotted the link. Optional.')
    enable_comments = models.BooleanField(default=True)
    posted_by = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    categories = models.ManyToManyField(Category)
    tags = TagField()

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title

    def save(self, force_insert = False, force_update = False):
        self.description_html = markdown(self.description)
        super(Link, self).save(force_insert, force_update)

    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_link_detail', (), {   'year': self.pub_date.strftime('%Y'),
                                                'month': self.pub_date.strftime('%b').lower(),
                                                'day': self.pub_date.strftime('%d'),
                                                'slug': self.slug })

# See http://blog.sveri.de/index.php?/categories/2-Django
try:
    tagging.register(Link, tag_descriptor_attr='etags')
except tagging.AlreadyRegistered:
    pass
