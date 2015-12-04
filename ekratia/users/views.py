# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from braces.views import LoginRequiredMixin

from .forms import UserForm
from .models import User
from ekratia.delegates.models import Delegate


class UserDetailView(LoginRequiredMixin, DetailView):
    """
    User Detail View.
    Displays the details for an user
    """
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['delegaters'] = Delegate.objects.filter(
            delegate=self.get_object()).prefetch_related('user')
        context['delegateds'] = Delegate.objects.filter(
            user=self.get_object()).prefetch_related('delegate')
        return context


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update Users View
    """

    form_class = UserForm

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    """
    List users view
    """
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
