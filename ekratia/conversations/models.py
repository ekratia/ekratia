from django.db import models
from django.utils.translation import ugettext_lazy as _
from config.settings import common
from ekratia.threads.models import Comment
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.utils import timezone


class Thread(models.Model):
    """
    Thread model:
    Used for conversations.
    """
    title = models.CharField(max_length=25, blank=False,
                             verbose_name=_('Subject'))
    slug = models.SlugField(max_length=50, db_index=True, unique=True)
    description = models.TextField(max_length=1000, blank=False,
                                   verbose_name=_('Message'))
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(common.AUTH_USER_MODEL)

    comment = models.OneToOneField(Comment, null=True, blank=True)
    num_comments = models.IntegerField(default=0)

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        if not self.slug:
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

        return reverse('conversations:detail', kwargs=kwargs)
