from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime


class ReferendumVotesManager(models.Manager):
    def open_votes(self, user, positive=True):
        expiration_time = timezone.now() - datetime.timedelta(
            hours=settings.REFERENDUM_EXPIRE_HOURS)
        queryset = self.get_queryset()
        queryset = queryset.filter(user=user)
        queryset = queryset.filter(
            referendum__open_time__isnull=False,
            referendum__open_time__gt=expiration_time)
        if positive:
            queryset = queryset.filter(value__gt=0)
        else:
            queryset = queryset.filter(value__lt=0)

        return queryset
