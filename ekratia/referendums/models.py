from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import PermissionDenied

from config.settings import common
from django.conf import settings
from ekratia.threads.models import Comment
from ekratia.core.graphs import GraphEkratia

from .managers import ReferendumVotesManager, ReferendumManager
import datetime
import logging
logger = logging.getLogger('ekratia')


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

    # Options: created, open, finished
    status = models.CharField(max_length=10, default='created')

    objects = ReferendumManager()

    class Meta:
        ordering = ['open_time', '-date']

    def check_status(self):
        """
        Method used to update status when necessary
        """
        if self.status == 'created':
            if self.is_open():
                self.status = 'open'
                self.save()
            if self.is_finished():
                self.status = 'finished'
                self.approved = self.is_approved()
                self.save()
        elif self.status == 'open':
            if self.is_finished():
                self.status = 'finished'
                self.approved = self.is_approved()
                self.save()

    def is_approved(self):
        """
        Get partial results and determines if It's approved or not
        """
        logger.debug("POINTS: %s" % self.points)
        return True if self.points > 0 else False

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

    def vote_process(self, user, value):
        """
        Processes a vote for the referendum
        returns the vote object
        """
        if value != -1 and value != 1:
            raise ValueError

        if not self.is_open():
            raise PermissionDenied("Referendum is not Open for voting")

        vote, created = ReferendumUserVote.objects.get_or_create(
                referendum=self,
                user=user
            )
        vote_deleted = False
        if not created:
            # If the vote is the same: Delete it
            if (value < 0 and vote.value < 0)\
                    or (value > 0 and vote.value > 0):
                vote.delete()
                vote_deleted = True
                self.update_user_vote(user)
        if not vote_deleted:
            vote.value = user.get_pagerank_value_referendum(self) * value
            vote.save()

        # Update other vote values that got affected
        affected_users = self.get_users_with_votes_on_referendum(
            exclude_user=user)
        for affected_user in affected_users:
            logger.debug("Update user vote: %s" % affected_user)
            self.update_user_vote(affected_user)

        self.update_totals()
        return vote, created

    def get_users_with_votes_on_referendum(self, exclude_user=None):
        from ekratia.users.models import User
        queryset = User.objects.filter(
            id__in=ReferendumUserVote.objects
                                     .open_votes()
                                     .filter(referendum=self)
                                     .values_list('user_id'))
        if exclude_user:
            queryset = queryset.exclude(id=exclude_user.id)

        return queryset

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

    def get_votes_list(self):
        return ReferendumUserVote.objects.filter(referendum=self)

    def get_graph(self):
        users_ids = self.get_votes_list().values_list('user_id', flat=True)
        graph = GraphEkratia()
        graph.add_users_ids(users_ids)
        return graph


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
            self.points = self.calculate_votes()
            self.save()
        return self

    def update_user_vote(self, user):
        user_vote_value = user.vote_count_for_referendum(self)
        try:
            vote = ReferendumUserVote.objects.get(referendum=self, user=user)
            vote.value = user_vote_value
            vote.save()
        except ReferendumUserVote.DoesNotExist:
            logger.debug("No Votes to update")

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
