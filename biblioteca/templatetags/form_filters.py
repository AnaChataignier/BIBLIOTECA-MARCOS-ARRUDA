# biblioteca/templatetags/form_filters.py

from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Adiciona uma classe CSS ao campo de formulário.
    """
    return value.as_widget(attrs={'class': arg})
