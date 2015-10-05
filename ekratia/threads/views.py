from django.views.generic import ListView, DetailView, CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from .models import Thread


class ThreadListView(ListView):
    """
    List of Threads
    """
    model = Thread
    template_name = 'threads/list.html'


class ThreadCreateView(CreateView):
    """
    Creates a Thread
    """
    model = Thread
    template_name = 'threads/create.html'
    fields = ['title', 'description', 'user']

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS,
                             _('New thread created'))
        return super(ThreadCreateView, self).form_valid(form)


class ThreadDetailView(DetailView):
    """
    Detail View for a Thread
    """
    model = Thread
    template_name = "threads/detail.html"
