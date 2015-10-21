from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from config.settings import common


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

    comment = models.OneToOneField('Comment', null=True, blank=True)

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        if not self.slug:
            title = self.title
            self.slug = original_slug = slugify(title)
            count = 0
            while Referendum.objects.filter(slug=self.slug).exists():
                count += 1
                self.slug = "%s-%i" % (original_slug, count)

        super(Referendum, self).save(*args, **kwargs)
