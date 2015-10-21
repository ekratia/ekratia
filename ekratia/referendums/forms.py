from django import forms
from .models import Referendum
from ekratia.threads.models import Comment


class ReferendumForm(forms.ModelForm):
    """
    Referendum Model Form
    """
    class Meta:
        model = Referendum
        exclude = ('user', 'slug',)

    def __init__(self, *args, **kwargs):
        super(ReferendumForm, self).__init__(*args, **kwargs)
        # self.fields['description'].widget = forms.Textarea(
        #     attrs={'rows': '2', 'ng-model': 'message', 'msd-elastic': '',
        #            'maxlength': '1000'})


class ReferendumCommentForm(forms.ModelForm):
    """
    Comment Referendums Model Form
    """
    class Meta:
        model = Comment
        fields = ('content',)
