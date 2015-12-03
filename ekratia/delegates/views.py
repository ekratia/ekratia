from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin


class UserDelegatesView(LoginRequiredMixin, TemplateView):
    """
    View with an Interface to list the delegated users and the available users
    to be delegated.
    """
    template_name = "delegates/user_delegates.html"
