from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from ekratia.topics.models import Topic


class Delegate(models.Model):
    """
    Delegate Model stores the delegations made by user in the system.
    """
    #: User delgating
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_set")
    #: User to delegate
    delegate = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name="delegate_set")
    topic = models.ForeignKey(Topic, null=True, blank=True)
    value = models.FloatField(validators=[
                              MinValueValidator(0.0),
                              MaxValueValidator(1.0)], default=0.0)

    def __unicode__(self):
        return "%s delegates to %s" % (self.user, self.delegate)
