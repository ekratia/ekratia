from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime


class ReferendumManager(models.Manager):
    def get_expiration_time(self):
        return timezone.now() - datetime.timedelta(
            hours=settings.REFERENDUM_EXPIRE_HOURS)

    def open(self):
        """
        Returns all the open referendums
        """
        expiration_time = self.get_expiration_time()
        queryset = self.get_queryset()
        queryset = queryset.filter(
            open_time__isnull=False,
            open_time__gt=expiration_time)

        return queryset

    def created(self):
        """
        Returns all the referendums not open for vote
        """
        queryset = self.get_queryset()
        queryset = queryset.filter(open_time__isnull=True)

        return queryset

    def finished(self):
        """
        Returns all the referendums finished
        """
        expiration_time = self.get_expiration_time()
        queryset = self.get_queryset()
        queryset = queryset.filter(
            open_time__isnull=False,
            open_time__lt=expiration_time)

        return queryset


class ReferendumVotesManager(models.Manager):
    def open_votes(self, user=None):
        """
        Returns all the votes of Open referendums
        user: Filter votes of this user only (optional)
        """
        expiration_time = timezone.now() - datetime.timedelta(
            hours=settings.REFERENDUM_EXPIRE_HOURS)
        queryset = self.get_queryset()
        if user:
            queryset = queryset.filter(user=user)
        queryset = queryset.filter(
            referendum__open_time__isnull=False,
            referendum__open_time__gt=expiration_time)

        return queryset
