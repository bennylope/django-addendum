from django import template
from django.template.base import TemplateSyntaxError
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from ..models import get_cached_snippet


register = template.Library()


def str_bool(val):
    if val.lower() == "true":
        return True
    elif val.lower() == "false":
        return False
    raise ValueError("{0} is not a string representation of a boolean".format(val))


def build_options(bits, tag_name):
    """
    Splits the tag keyword arguments into usable values.
    """

    options = {}

    for bit in bits:
        try:
            option, val = bit.split('=')
        except ValueError:
            raise TemplateSyntaxError("%s has bad or badly formed option arguments." % tag_name)

        if option not in ['safe', 'richtext', 'template', 'language']:
            raise TemplateSyntaxError("%s recieved an invalid option." % tag_name)

        # Backwards compatibility
        if option == 'richtext':
            option = 'safe'

        options.update({option: val})

    return options


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

    try:
        tag_name = token.split_contents()
        bits = token.split_contents()[1:]
    except IndexError:
        raise TemplateSyntaxError("%s tag takes at least one argument" % bits[0])

    key = bits[0]
    options = build_options(bits[1:], tag_name)

    return SnippetNode(nodelist, key, **options)


class SnippetNode(template.Node):

    safe = False
    template = False
    language = ''

    def __init__(self, nodelist, key, **options):
        self.nodelist = nodelist
        self.key = template.Variable(key)
        for k, v in options.items():
            setattr(self, k, template.Variable(v))

    def render(self, context):

        # Handle key as context variable or key as string
        try:
            key = self.key.resolve(context)
        except AttributeError:
            key = self.key[1:-1]

        if self.language != '':
            try:
                language = self.language.resolve(context)
            except AttributeError:
                language = self.language[1:-1]
        else:
            language = context.get('LANGUAGE_CODE', self.language)

        snippet = get_cached_snippet(key, language)

        if snippet is None:
            output = self.nodelist.render(context)
            return output

        if self.template:
            if self.safe:
                context.autoescape = False
                return mark_safe(template.Template(snippet).render(context))
            return template.Template(snippet).render(context)

        if self.safe:
            return mark_safe(snippet)

        return conditional_escape(snippet)
