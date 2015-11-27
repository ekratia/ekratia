import locale

from django import template
from django.core.urlresolvers import resolve, reverse
from django.utils.translation import activate, get_language

register = template.Library()
locale.setlocale(locale.LC_ALL, '')

@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    path = context['request'].path
    url_parts = resolve( path )
    url = path
    cur_language = get_language()

    if url_parts.url_name == 'home_page':
        url_parts.url_name = 'home_i18n'
    try:
        activate(lang)
        url = reverse( url_parts.view_name, kwargs=url_parts.kwargs )
    finally:
        activate(cur_language)
    return "%s" % url
