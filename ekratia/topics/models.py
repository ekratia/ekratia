from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey("self", blank=True, null=True)

    def __unicode__(self):
        return self.name
