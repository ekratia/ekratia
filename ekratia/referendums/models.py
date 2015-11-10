from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import Sum

from config.settings import common
from django.conf import settings
from ekratia.threads.models import Comment

from .managers import ReferendumVotesManager
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

    # Total Value of the Referndum
    points = models.FloatField(default=0)

    # Total Values for Stats
    total_yes = models.FloatField(default=0.0)
    total_no = models.FloatField(default=0.0)
    total_votes = models.FloatField(default=0.0)
    total_users = models.IntegerField(default=0)

    # True If approved, False if not approved, None not set yet
    approved = models.NullBooleanField(null=True, blank=True)

    # Comment thread
    comment = models.OneToOneField(Comment, null=True, blank=True)
    # Rating due to the comments, used to establish trendy referendums
    comment_points = models.FloatField(default=0.0)

    def is_open(self):
        """
        Method to establish id Referendum is open for vote.
        """
        if not self.open_time:
            return False
        else:
            return True if self.open_remaining_time() >\
                datetime.timedelta() else False

    def is_finished(self):
        """
        Method to establish id Referendum is open for vote.
        """
        if not self.open_time:
            return False
        else:
            return True if not self.is_open() else False

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

    def calculate_votes(self):
        """
        Calculates total votes based on ReferendumUserVote
        """
        self.points = ReferendumUserVote.objects.filter(referendum=self)\
            .aggregate(count=Sum('value'))['count']
        if self.points is None:
            self.points = 0.0
        self.save()
        return self.points

    def get_count_votes(self):
        """
        Calculates total votes for referenudm
        """
        return ReferendumUserVote.objects.filter(referendum=self).count()

    def get_total_votes(self):
        """
        Calculates total votes for referenudm
        """
        return self.calculate_votes()

    def get_num_positive_votes(self):
        """
        Returns total positive votes
        """
        votes = ReferendumUserVote.objects.filter(
            referendum=self,
            value__gt=0).aggregate(count=Sum('value'))['count']
        return votes if votes else 0

    def get_num_negative_votes(self):
        """
        Return the total negative votes
        """
        votes = ReferendumUserVote.objects.filter(
            referendum=self,
            value__lt=0).aggregate(count=Sum('value'))['count']
        return -votes if votes else 0

    def get_total_votes_absolute(self):
        """
        Returns Total ov votes for the referendum
        """
        return self.get_num_positive_votes() + self.get_num_negative_votes()

    def update_totals(self):
        """
        Update totals in the Database
        Returns the updated referendum
        """
        if self.is_open():
            self.total_yes = self.get_num_positive_votes()
            self.total_no = self.get_num_negative_votes()
            self.total_votes = self.total_yes + self.total_no
            self.total_users = self.get_count_votes()
            self.save()
        return self

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
    date = models.DateTimeField(default=timezone.now)

    # Custom manager
    objects = ReferendumVotesManager()
