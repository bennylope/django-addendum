from django import template
from django.template.base import TemplateSyntaxError
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from ..models import Snippet


register = template.Library()


@register.tag
def snippet(parser, token):
    """
    Demarcates replaceable text, outputs the wrapped text or the text of a
    snippet with matching key.

    Examples::

        {% snippet 'greeting' %}Hello world{% endsnippet %}

        {% snippet 'greeting' richtext=True %}<p>Hey!</p>{% endsnippet %}
    """
    nodelist = parser.parse(('endsnippet',))
    parser.delete_first_token()
    options = {}

    try:
        # split_contents() knows not to split quoted strings.
        tag_name, key, option_kwargs = token.split_contents()
        try:
            option, val = option_kwargs.split('=')
        except ValueError:
            raise TemplateSyntaxError("Bad or badly formed option arguments.")
        else:
            if option not in ['richtext', 'template']:
                raise TemplateSyntaxError("Invalid option; only 'richtext' and 'template' can be used.")
            if val == "True":
                options.update({option: True})
            elif val == "False":
                options.update({option: False})
            else:
                raise TemplateSyntaxError("Invalid option value; you must specify a Boolean value.")

    except ValueError:
        tag_name, key = token.split_contents()
    return SnippetNode(nodelist, key[1:-1], **options)


class SnippetNode(template.Node):

    richtext = False
    template = False

    def __init__(self, nodelist, key, **options):
        self.nodelist = nodelist
        self.key = key
        for k, v in options.items():
            setattr(self, k, v)

    def render(self, context):
        key = self.key
        snippet = Snippet.objects.get_from_cache(key=key)
        if snippet is None:
            output = self.nodelist.render(context)
            return output

        if self.template:
            return template.Template(snippet.text).render(context)

        if self.richtext:
            return mark_safe(snippet.text)

        return conditional_escape(snippet.text)
