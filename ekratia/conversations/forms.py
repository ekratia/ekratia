from django import forms
from .models import Thread


class ThreadForm(forms.ModelForm):
    """
    Thread Model Form
    """
    class Meta:
        model = Thread
        exclude = ('user', 'slug', 'comment', 'date')

    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(
            attrs={'rows': '2', 'ng-model': 'message', 'msd-elastic': '',
                   'maxlength': '1000'})

