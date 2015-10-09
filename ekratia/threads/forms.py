from django import forms
from .models import Thread, Comment


class ThreadForm(forms.ModelForm):
    """
    Thread Model Form
    """
    class Meta:
        model = Thread
        exclude = ('user', 'slug',)

    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(
            attrs={'rows': '2', 'ng-model': 'message', 'msd-elastic': '',
                   'maxlength': '1000'})


class ThreadCommentForm(forms.ModelForm):
    """
    Comment Threads Model Form
    """
    class Meta:
        model = Comment
        fields = ('content',)
