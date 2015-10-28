from django import forms
from .models import Comment


class ThreadCommentForm(forms.ModelForm):
    """
    Comment Threads Model Form
    """
    class Meta:
        model = Comment
        fields = ('content',)
