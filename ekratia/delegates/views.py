from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin


class UserDelegatesView(LoginRequiredMixin, TemplateView):
    """docstring for UserDelegatesView"""
    template_name = "delegates/user_delegates.html"
