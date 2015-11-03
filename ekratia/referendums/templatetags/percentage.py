from django import template
from django.utils.formats import number_format

register = template.Library()


@register.filter(name='percentage')
def percentage(fraction, population):
    try:
        return "%.2f%%" % ((float(fraction) / float(population)) * 100)
    except ValueError:
        return 0
    except ZeroDivisionError:
        return 0
