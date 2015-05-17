from django.db import models


from django.db import models
from django import forms
from django.contrib.auth.models import User
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
