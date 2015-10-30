from django.views.generic import ListView, DetailView, CreateView, RedirectView
from django.contrib import messages

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

        referendum_text = "%s \n %s " % (self.object.text_remove_rules,
                                         self.object.text_add_rules)

        root_comment = Comment.add_root(content=referendum_text,
                                        user_id=self.request.user.id)
        root_comment.save()
        self.object.comment = root_comment

        self.object = form.save(commit=True)
        self.object.title = "Referendum %i " % self.object.id
        self.object.save()

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


class ReferendumOpenView(RedirectView):
    """
    Open Referendum and redirects back to Referendum
    """
    permanent = False
    pattern_name = 'referendums:detail'

    def get_redirect_url(self, *args, **kwargs):
        # referendum = get_object_or_404(Referendum, pk=kwargs['pk'])
        messages.success(self.request, 'Referendum Ready to Vote!')
        return super(ReferendumOpenView, self).get_redirect_url(*args, **kwargs)
