from django import forms
from string import Template
from django.utils.safestring import mark_safe
from django.conf import settings

class ToggleWidget(forms.widgets.CheckboxInput):
    class Media:
        js = ("https://gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min.js",)

    def __init__(self, attrs=None, *args, **kwargs):
        attrs = attrs or {}

        default_options = {
            'toggle': 'toggle',
            'offstyle': 'danger'
        }
        options = kwargs.get('options', {})
        default_options.update(options)
        for key, val in default_options.items():
            attrs['data-' + key] = val

        super().__init__(attrs)

class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, **kwargs):
        html = Template("""<img class="rounded-circle account-img" src="$media$link"/>""")
        return mark_safe(html.substitute(media=settings.MEDIA_URL, link=value))
