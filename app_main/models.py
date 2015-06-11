from django.db import models

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


from django.db import models
from config.settings import common

import datetime

class Thread(models.Model):

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
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


class Topic(models.Model):
    name = models.CharField(max_length=200, default="Topic Name")
    subtopic = models.ForeignKey("self", blank=True, null=True)

    def __unicode__(self):
        return self.name

class Proposal(models.Model):
    thread = models.ForeignKey(Thread)
    topics = models.ManyToManyField(Topic, verbose_name="list of topics", through='ProposalTopicWeight', through_fields=('proposal', 'topic'))
    summary = models.CharField(max_length=200)
    rule = models.TextField()
    expiration_date = models.DateField(default=datetime.datetime(2015+18, 5, 17, 20, 44, 15, 407805))

    def __unicode__(self):
        return self.thread.title

    def pollResults():
        return

class ProposalTopicWeight(models.Model):
    proposal = models.ForeignKey(Proposal)
    topic = models.ForeignKey(Topic)
    weight = models.DecimalField(max_digits=3, decimal_places=2)

    def save(self, *args, **kwargs):
        self.validateWeith()
        return super(ProposalTopicWeight, self).save(*args, **kwargs)

    def validateWeith(self):
        total = 100
        if total > 100:
            raise ValueError('The weight assigned for this topic is incorrect. The total weight exceeds 100')
        # validate the weight according the topics in the proposal
        # save many


class Vote(models.Model):
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    weight = models.DecimalField(max_digits=3, decimal_places=2)
    agree = models.BooleanField()

    class Meta:
        abstract = True


class ProposalVote(Vote):
    proposal = models.ForeignKey(Proposal)

    def save(self, *args, **kwargs):
        self.calculateWeight();
        self.updateFollowing()
        return super(Vote, self).save(*args, **kwargs)

    def vote(Voter, proposal, agree):
        proposalVote = ProposalVote(user=Voter.user, weight=Voter.weight, proposal=proposal, agree=agree)
        return super(ProposalVote, self).save(*args, **kwargs)

    @staticmethod
    def results(proposal):
        return ProposalVote.objects.values('agree').filter(proposal=proposal).annotate(total=sum('weight'))

    def calculateWeight(self):
        pass
        # self.weight = 100
        # Call users to get followers and calculate price
        # based on topic of the Proposal
        # Take into account the votes

    def updateFollowing(self):
        pass
        # Call user to get following and update Proposals with
        # saveAll


class CommentVote(Vote):
    comment = models.ForeignKey(Proposal)

class Voter(models.Model):
    weight = models.DecimalField(max_digits=12, decimal_places=2)

    @staticmethod
    def mostPromminentVoters(limit=10, offset=0):
        return Voter.objects.order_by('weight')[offset:limit]

class Delegate(models.Model):
    user = models.ForeignKey(common.AUTH_USER_MODEL, related_name="user_set")
    delegate = models.ForeignKey(common.AUTH_USER_MODEL, related_name="delegate_set")
    topic = models.ForeignKey(Topic)

    @staticmethod
    def delegates(userId):
        return Delegate.objects.filter(user=userId)
