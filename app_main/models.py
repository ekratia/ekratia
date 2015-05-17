from django.db import models


from django.db import models
from django import forms
from config.settings import common

class Thread(models.Model):

    description = models.CharField(max_length=1000)
    title = models.CharField(max_length=30)
    #date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.description



class Comment(models.Model):

    content = models.CharField(max_length=30)
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    #date = models.DateTimeField(auto_now_add=True)
    #path = IntegerArrayField(blank=True, editable=False)
    depth = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.description

class CommentForm(forms.ModelForm):
    #Hidden value to get a child's parent
    parent = forms.CharField(widget=forms.HiddenInput(
                            attrs={'class': 'parent'}), required=False)

    class Meta:
        model = Comment
        fields = ('content',)


class Topic(models.Model):
    subtopic = models.ForeignKey("self")


class Project(models.Model):
    thread = models.ForeignKey(Thread)
    topics = models.ManyToManyField(Topic, verbose_name="list of topics", through='ProjectTopicWeight', through_fields=('project', 'topic'))

    def pollResults():
        return

class ProjectTopicWeight(models.Model):
    project = models.ForeignKey(Project)
    topic = models.ForeignKey(Topic)
    weight = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.validateWeith()
        return super(TopicWeight, self).save(*args, **kwargs)

    def validateWeith():
        total = 100
        if total > 100:
            raise ValueError('The weight assigned for this topic is incorrect. The total weight exceeds 100')
        # validate the weight according the topics in the project
        # save many

class Vote(models.Model):
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    weight = models.PositiveIntegerField()
    agree = models.BooleanField()

    class Meta:
        abstract = True

class ProjectVote(Vote):
    project = models.ForeignKey(Project)

    def save(self, *args, **kwargs):
        self.weight = self.calculateWeith();
        self.updateFollowing()
        return super(Vote, self).save(*args, **kwargs)

    def calculateWeight():
        pass
        # Call users to get followers and calculate price
        # based on topic of the Project
        # Take into account the votes 

    def updateFollowing():
        pass
        # Call user to get following and update Projects with 
        # saveAll


class CommentVote(Vote):
    comment = models.ForeignKey(Project)


class Delegate(models.Model):
    user = models.ForeignKey(common.AUTH_USER_MODEL, related_name="user_set")
    delegate = models.ForeignKey(common.AUTH_USER_MODEL, related_name="delegate_set")
    topic = models.ForeignKey(Topic)








