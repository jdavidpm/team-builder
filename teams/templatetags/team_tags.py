from django import template
from urllib import parse
from django.http import QueryDict
register = template.Library()

@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)

@register.filter
def get_class(value):
    return value.__class__.__name__

@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    previous = request.META.get('HTTP_REFERER')
    dict_prev = QueryDict('', mutable=True)
    dict_prev.update(dict(parse.parse_qsl(parse.urlsplit(previous).query)))
    for k, v in dict_prev.items():
        updated[k] = v
    for k, v in kwargs.items():
        updated[k] = v
    print(updated.urlencode())
    return updated.urlencode()