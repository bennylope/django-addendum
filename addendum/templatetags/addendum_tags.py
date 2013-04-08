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
        tag_name = token.split_contents()
        bits = token.split_contents()[1:]
    except IndexError:
        raise TemplateSyntaxError("%s tag takes at least one argument" % bits[0])

    key = bits[0]

    for bit in bits[1:]:
        try:
            option, val = bit.split('=')
        except ValueError:
            raise TemplateSyntaxError("%s has bad or badly formed option arguments." % tag_name)

        if option not in ['safe', 'richtext', 'template']:
            raise TemplateSyntaxError("%s recieved an invalid option." % tag_name)

        if option == 'richtext':
            option = 'safe'

        if val == "True":
            options.update({option: True})
        elif val == "False":
            options.update({option: False})
        else:
            raise TemplateSyntaxError("%s received an invalid option value." % tag_name)

    return SnippetNode(nodelist, key, **options)


class SnippetNode(template.Node):

    safe = False
    template = False

    def __init__(self, nodelist, key, **options):
        self.nodelist = nodelist
        self.key = template.Variable(key)
        for k, v in options.items():
            setattr(self, k, v)

    def render(self, context):
        try:
            key = self.key.resolve(context)
        except AttributeError:
            key = self.key[1:-1]
        snippet = Snippet.objects.get_from_cache(key=key)
        if snippet is None:
            output = self.nodelist.render(context)
            return output

        if self.template:
            if self.safe:
                context.autoescape = False
                return mark_safe(template.Template(snippet.text).render(context))
            return template.Template(snippet.text).render(context)

        if self.safe:
            return mark_safe(snippet.text)

        return conditional_escape(snippet.text)
