from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime


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
