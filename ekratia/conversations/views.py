from django.views.generic import ListView, DetailView, CreateView

from braces.views import LoginRequiredMixin

from .models import Thread, Comment
from .forms import ThreadForm
from ekratia.threads.forms import ThreadCommentForm


class ThreadListView(ListView):
    """
    List of Threads
    """
    model = Thread
    template_name = 'conversations/list.html'


class ThreadCreateView(LoginRequiredMixin, CreateView):
    """
    Creates a Thread
    """
    model = Thread
    template_name = 'conversations/create.html'
    form_class = ThreadForm

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        root_comment = Comment.add_root(content=self.object.description,
                                        user_id=self.request.user.id)
        root_comment.save()
        self.object.comment = root_comment

        self.object = form.save(commit=True)

        # messages.add_message(self.request, messages.SUCCESS,
        #                      _('Conversation has been created'))
        return super(ThreadCreateView, self).form_valid(form)


class ThreadDetailView(DetailView):
    """
    Detail View for a Thread
    """
    model = Thread
    template_name = "conversations/detail.html"

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = super(ThreadDetailView, self).get_context_data(**kwargs)
        context['form_comment'] = ThreadCommentForm
        self.object.count_comments()
        return context
