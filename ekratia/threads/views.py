from django.views.generic import ListView, DetailView, CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from .models import Thread
from .forms import ThreadForm


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
    form_class = ThreadForm

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object = form.save(commit=True)

        messages.add_message(self.request, messages.SUCCESS,
                             _('New thread created'))
        return super(ThreadCreateView, self).form_valid(form)


class ThreadDetailView(DetailView):
    """
    Detail View for a Thread
    """
    model = Thread
    template_name = "threads/detail.html"
