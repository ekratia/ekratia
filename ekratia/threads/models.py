from django.db import models
from config.settings import common
from django.utils.text import slugify
from django.core.urlresolvers import reverse


class Thread(models.Model):
    """
    Thread model:
    Used for conversations.
    """
    title = models.CharField(max_length=30, blank=False)
    slug = models.SlugField(max_length=250, db_index=True, unique=True)
    description = models.TextField(max_length=1000, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(common.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        title = self.title
        self.slug = original_slug = slugify(title)
        count = 0
        while Thread.objects.filter(slug=self.slug).exists():
            count += 1
            self.slug = "%s-%i" % (original_slug, count)

        super(Thread, self).save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
        }

        return reverse('threads:detail', kwargs=kwargs)


class Comment(models.Model):
    """
    Comment Model:
    Comments under Threads and other comments
    """
    content = models.CharField(max_length=30, blank=False)
    thread = models.ForeignKey(Thread)
    parent = models.ForeignKey('Comment', blank=True, null=True)
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    date = models.DateTimeField(auto_now_add=True)
    # path = IntegerArrayField(blank=True, editable=False)
    depth = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.content
