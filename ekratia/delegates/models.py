from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from ekratia.topics.models import Topic


class Delegate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_set")
    delegate = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name="delegate_set")
    topic = models.ForeignKey(Topic, null=True, blank=True)
    value = models.FloatField(validators=[
                              MinValueValidator(0.0),
                              MaxValueValidator(1.0)], default=0.0)

    @staticmethod
    def delegates(user_id):
        return Delegate.objects.filter(user=user_id)

    @staticmethod
    def topic_delegates(user_id, topic_id):
        return Delegate.objects.filter(user=user_id, topic_id=topic_id)
