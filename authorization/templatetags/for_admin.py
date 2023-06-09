from django import template

from authorization.services import get_count_new_requests_for_output

register = template.Library()


@register.simple_tag(name='get_count_new_requests_for_output')
def get_count():
    return get_count_new_requests_for_output()
