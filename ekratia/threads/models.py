from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum

from config.settings import common

from treebeard.mp_tree import MP_Node, MP_NodeManager
from collections import OrderedDict
import datetime


class Thread(models.Model):
    """
    Thread model:
    Used for conversations.
    """
    title = models.CharField(max_length=250, blank=False,
                             verbose_name=_('Subject'))
    slug = models.SlugField(max_length=250, db_index=True, unique=True)
    description = models.TextField(max_length=1000, blank=False,
                                   verbose_name=_('Message'))
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(common.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
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

        return reverse('threads:detail', kwargs=kwargs)


class ThreadUserVote(models.Model):
    """
    ThreadUserVote Model:
    Stores votes from users to Threads
    """
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    thread = models.ForeignKey(Thread)
    value = models.IntegerField(default=1)


class CommentManager(MP_NodeManager):
    """
    Manager for the comment model.
    Allows custom operation on the tree.
    """
    def build_tree(self, parent=None, order_by=None):
        if parent is None:
            tree = Comment.get_tree()
            parent_depth = 1
        else:
            tree = Comment.get_tree(parent=parent)
            parent_depth = parent.depth

        if order_by is not None:
            tree = tree.order_by(order_by)

        output_tree = OrderedDict()

        leafs = list(tree)
        depth = parent_depth - 1
        traversed_path = []

        def get_chunks(path, steplen):
            output=[]
            for chunk in range(0,len(path)/steplen):
                output.append(path[chunk*steplen:(chunk+1)*steplen])
            return output

        while len(leafs)>0:
            depth+= 1
            moved = []
            for key, leaf in enumerate(leafs):
                if leaf.depth == depth:
                    parent_path = get_chunks(leaf.path[(parent_depth-1)*Comment.steplen:], Comment.steplen)
                    path = output_tree

                    for chunk in range(0,(len(parent_path))-1):
                        path = path[parent_path[chunk]][1]
                    path[parent_path[-1]] = [{'content':leaf.content, 'user': leaf.user.pk,}, OrderedDict()]
                    moved.append(key)

            for to_delete in reversed(moved):
                del(leafs[to_delete])
            if depth > 50:
                raise Exception
        return output_tree


class Comment(MP_Node):
    """
    Comment Model:
    Comments under Threads and other comments
    """
    content = models.TextField(max_length=1000, blank=False,
                               verbose_name=_('Comment'))
    thread = models.OneToOneField(Thread, null=True, blank=True)
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    date = models.DateTimeField(default=datetime.datetime.now)
    points = models.IntegerField(default=0)
    objects = CommentManager()

    def calculate_votes(self):
        """
        Calculates total votes based on CommentUserVote
        """
        self.points = CommentUserVote.objects.filter(comment=self)\
            .aggregate(count=Sum('value'))['count']
        if self.points is None:
            self.points = 0
        self.save()
        return self.points

    node_order_by = ['date']

    def __unicode__(self):
        return self.content


class CommentUserVote(models.Model):
    """
    CommentUserVote Model:
    Stores votes from users to Comments
    """
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    comment = models.ForeignKey(Comment)
    value = models.IntegerField(default=1)
