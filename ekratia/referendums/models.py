from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone

from config.settings import common
from django.conf import settings
from ekratia.threads.models import Comment

import datetime


class Referendum(models.Model):
    """
    Referendum model:
    """
    title = models.CharField(max_length=25, blank=False,
                             verbose_name=_('Subject'))
    slug = models.SlugField(max_length=50, db_index=True, unique=True)
    text_remove_rules = models.TextField(
        max_length=1000, blank=False,
        verbose_name=_('Text that this referendum will remove from our rules'))
    text_add_rules = models.TextField(
        max_length=1000, blank=False,
        verbose_name=_('Text that this referendum will add to our rules'))
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    open_time = models.DateTimeField(null=True, blank=True)

    comment = models.OneToOneField(Comment, null=True, blank=True)

    def is_open(self):
        """
        Method to establish id Referendum is open for vote.
        """
        if not self.open_time:
            return False
        else:
            return True if self.open_remaining_time() >\
                datetime.timedelta() else False

    def open_remaining_time(self):
        """
        Returns the remaining time for vote.
        """
        end_time = self.end_time()
        now = timezone.now()
        remaining_time = end_time - now if end_time > now\
            else datetime.timedelta()
        return remaining_time

    def end_time(self):
        return self.open_time\
            + datetime.timedelta(hours=settings.REFERENDUM_EXPIRE_HOURS)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            title = self.title
            self.slug = original_slug = slugify(title)
            count = 0
            while Referendum.objects.filter(slug=self.slug).exists():
                count += 1
                self.slug = "%s-%i" % (original_slug, count)

        super(Referendum, self).save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
        }
        return reverse('referendums:detail', kwargs=kwargs)


class ReferendumUserVote(models.Model):
    """
    ReferendumUserVote Model:
    Stores votes from users to Referendums
    """
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    referendum = models.ForeignKey(Referendum)
    value = models.FloatField(default=1)
    date = models.DateTimeField(default=timezone.now())
