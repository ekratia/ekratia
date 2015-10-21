from django.views.generic import ListView, DetailView, CreateView

from braces.views import LoginRequiredMixin

from .models import Referendum
from ekratia.threads.models import Comment
from .forms import ReferendumForm, ReferendumCommentForm


class ReferendumListView(ListView):
    """
    List of Referendums
    """
    model = Referendum
    template_name = 'referendums/list.html'


class ReferendumCreateView(LoginRequiredMixin, CreateView):
    """
    Creates a Referendum
    """
    model = Referendum
    template_name = 'referendums/create.html'
    form_class = ReferendumForm

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
        return super(ReferendumCreateView, self).form_valid(form)


class ReferendumDetailView(DetailView):
    """
    Detail View for a Referendum
    """
    model = Referendum
    template_name = "referendums/detail.html"

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = super(ReferendumDetailView, self).get_context_data(**kwargs)
        context['form_comment'] = ReferendumCommentForm
        return context
