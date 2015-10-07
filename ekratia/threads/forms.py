from django import forms
from .models import Thread, Comment


class ThreadForm(forms.ModelForm):
    """
    Thread Model Form
    """
    class Meta:
        model = Thread
        # fields = ('title', 'description', 'user',)
        exclude = ('user', 'slug',)


class ThreadCommentForm(forms.ModelForm):
    """
    Comment Threads Model Form
    """
    class Meta:
        model = Comment
        fields = ('content',)
