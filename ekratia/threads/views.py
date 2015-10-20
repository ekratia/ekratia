from django.views.generic import ListView, DetailView, CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from braces.views import LoginRequiredMixin

from .models import Thread
from .forms import ThreadForm, ThreadCommentForm


class ThreadListView(ListView):
    """
    List of Threads
    """
    model = Thread
    template_name = 'threads/list.html'


class ThreadCreateView(LoginRequiredMixin, CreateView):
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

        # messages.add_message(self.request, messages.SUCCESS,
        #                      _('Conversation has been created'))
        return super(ThreadCreateView, self).form_valid(form)


class ThreadDetailView(DetailView):
    """
    Detail View for a Thread
    """
    model = Thread
    template_name = "threads/detail.html"

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = super(ThreadDetailView, self).get_context_data(**kwargs)
        context['form_comment'] = ThreadCommentForm
        return context
