from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, CreateView, RedirectView

from braces.views import LoginRequiredMixin

from .models import Referendum, ReferendumUserVote
from ekratia.threads.models import Comment
from .forms import ReferendumForm, ReferendumCommentForm

import logging
import datetime

logger = logging.getLogger('ekratia')


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
        if self.request.user.is_authenticated():
            context['user_vote'] = self.request.user.\
                get_vote_referendum(self.object)
            # vote_count_for_referendum
            context['user_vote_value'] = self.request.user.\
                vote_count_for_referendum(self.object)

        context['object'] = self.object.update_totals()

        if settings.DEBUG:
            logger.debug("Vote details for %s" % self.object.title)
            for vote in self.object.get_votes_list():
                logger.debug("User: %s  Value: %s" % (vote.user, vote.value))

        return context


class ReferendumOpenView(LoginRequiredMixin, RedirectView):
    """
    Open Referendum and redirects back to Referendum
    """
    permanent = False
    pattern_name = 'referendums:detail'

    def get_redirect_url(self, *args, **kwargs):
        referendum = get_object_or_404(Referendum, slug=kwargs['slug'])

        if referendum.user != self.request.user:
            raise HttpResponseForbidden

        if not referendum.is_open():
            referendum.open_time = datetime.datetime.now()
            referendum.save()
            messages.success(self.request, _('Referendum Ready to Vote!'))
        else:
            messages.error(self.request, _('Referendum is already Open'))

        return super(ReferendumOpenView, self).\
            get_redirect_url(*args, **kwargs)


class ReferendumVoteView(LoginRequiredMixin, ReferendumDetailView):
    """
    Detail View for a Referendum
    """
    template_name = "referendums/vote.html"

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = super(ReferendumVoteView, self).get_context_data(**kwargs)
        return context


class ReferendumProcessVoteView(LoginRequiredMixin, RedirectView):
    """
    Open Referendum and redirects back to Referendum
    """
    permanent = False
    pattern_name = 'referendums:detail'

    def get_redirect_url(self, *args, **kwargs):
        logger.debug("Procesing Vote")
        referendum = get_object_or_404(Referendum, slug=kwargs['slug'])

        # Accepts yes or no
        vote_answer = kwargs['value']
        if vote_answer != 'yes' and vote_answer != 'no':
            logger.error("Invalid Vote Value")
            raise Http404("Invalid Vote Value")

        logger.debug(
            "Procesing Vote %s, Value %s" % (referendum.title, vote_answer))

        if referendum.is_open():
            logger.debug("Referendum is open")
            # Positive or negative depending on answer
            vote_value = 1 if vote_answer == 'yes' else -1
            referendum.vote_process(self.request.user, vote_value)

            messages.success(self.request, _('We got your Vote. Thanks!'))
        else:
            messages.error(self.request, _('Referendum is Closed'))
        return reverse('referendums:detail', kwargs={'slug': referendum.slug})
