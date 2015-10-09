from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum

from config.settings import common

from treebeard.mp_tree import MP_Node
import datetime


class Thread(models.Model):
    """
    Thread model:
    Used for conversations.
    """
    title = models.CharField(max_length=30, blank=False,
                             verbose_name=_('Subject'))
    slug = models.SlugField(max_length=250, db_index=True, unique=True)
    description = models.TextField(max_length=1000, blank=False,
                                   verbose_name=_('Message'))
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


class ThreadUserVote(models.Model):
    """
    ThreadUserVote Model:
    Stores votes from users to Threads
    """
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    thread = models.ForeignKey(Thread)
    value = models.IntegerField(default=1)


class Comment(MP_Node):
    """
    Comment Model:
    Comments under Threads and other comments
    """
    content = models.TextField(max_length=30, blank=False,
                               verbose_name=_('Comment'))
    thread = models.OneToOneField(Thread, null=True, blank=True)
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    date = models.DateTimeField(default=datetime.datetime.now)
    points = models.IntegerField(default=0)

    def calculate_votes(self):
        """
        Calculates total votes based on CommentUserVote
        """
        self.points = CommentUserVote.objects.filter(comment=self)\
            .aggregate(count=Sum('value'))['count']
        if self.points is None:
            self.points = 0
        self.save()
        return self.points

    node_order_by = ['date']

    def __unicode__(self):
        return self.content


class CommentUserVote(models.Model):
    """
    CommentUserVote Model:
    Stores votes from users to Comments
    """
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    comment = models.ForeignKey(Comment)
    value = models.IntegerField(default=1)
