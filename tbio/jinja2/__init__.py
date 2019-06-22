import jinja2

from django.urls import reverse
from django.utils.html import urlize
from django.templatetags.static import static
from django.contrib.humanize.templatetags import humanize


def environment(**options):
    env = jinja2.Environment(**options)
    env.undefined = jinja2.StrictUndefined
    env.globals.update({
        'static': static,
        'url': reverse,
        'humanize': humanize,
        'urlize': urlize,
    })
    return env
