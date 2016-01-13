from django.views.generic import TemplateView
from django.utils.translation import get_language


class HomePageView(TemplateView):
    """
    List of Threads
    """
    template_name = 'pages/home.html'

    def get_template_names(self):
        templates = super(HomePageView, self).get_template_names()
        language = get_language()
        if language == 'es':
            templates = ['pages/home_es.html']
        return templates
