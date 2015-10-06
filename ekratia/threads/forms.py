from django import forms
from .models import Thread


class ThreadForm(forms.ModelForm):
    """
    Thread Model Form
    """
    class Meta:
        model = Thread
        # fields = ('title', 'description', 'user',)
        exclude = ('user', 'slug',)
