import logging

from django import template
from django.template.base import TemplateSyntaxError
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from addendum.models import get_cached_snippet, Snippet

logger = logging.getLogger(__name__)
register = template.Library()


def build_options(bits, tag_name):
    """
    Splits the tag keyword arguments into usable values.
    """

    options = {}

    for bit in bits:
        try:
            option, val = bit.split("=")
        except ValueError:
            raise TemplateSyntaxError(
                "%s has bad or badly formed option arguments." % tag_name
            )

        # Backwards compatibility
        if option == "richtext":
            option = "safe"

        if option not in ["safe", "template", "language"]:
            raise TemplateSyntaxError("%s received an invalid option." % tag_name)

        options.update({option: val})

    return options


@register.tag
def snippet(parser, token):
    """
    Demarcates replaceable text, outputs the wrapped text or the text of a
    snippet with matching key.

    Examples::

        {% snippet 'greeting' %}Hello world{% endsnippet %}

        {% snippet 'greeting' safe=True %}<p>Hey!</p>{% endsnippet %}
    """
    nodelist = parser.parse(("endsnippet",))
    parser.delete_first_token()

    bits = token.split_contents()
    tag_name = bits[0]
    try:
        key = bits[1]
    except IndexError:
        raise TemplateSyntaxError("%s tag takes at least one argument" % tag_name)

    options = build_options(bits[2:], tag_name)

    return SnippetNode(nodelist, key, **options)


class SnippetNode(template.Node):

    safe = None
    template = None
    language = None

    def __init__(self, nodelist, key, **options):
        self.nodelist = nodelist
        self.key = template.Variable(key)
        for k, v in options.items():
            setattr(self, k, template.Variable(v))

    def get_snippet_defaults(self, context, key, language):
        snippet = get_cached_snippet(key, language)
        default_text = self.nodelist.render(context)

        if snippet is None:
            snippet = Snippet(key=key, text=default_text)
            snippet.save()
            return default_text

        return snippet, default_text

    def render_as_template(self, context, snippet, default_text):
        if self.safe:
            old_autoescape = context.autoescape
            context.autoescape = False
            try:
                rendered = template.Template(snippet).render(context)
            except TemplateSyntaxError:
                logger.exception("Template error in snippet")
                return default_text
            context.autoescape = old_autoescape
            return mark_safe(rendered)

        try:
            return template.Template(snippet).render(context)
        except TemplateSyntaxError:
            logger.exception("Template error in snippet")
            return default_text

    def render(self, context):
        key = self.key.resolve(context)

        if self.language:
            language = self.language.resolve(context)
        else:
            language = context.get("LANGUAGE_CODE", "")

        snippet = get_cached_snippet(key, language)
        default_text = self.nodelist.render(context)

        if snippet is None:
            snippet = Snippet(key=key, text=default_text)
            snippet.save()
            return default_text

        if self.template:
            try:
                self.template = self.template.resolve(context)
            except AttributeError:
                self.template = True

        if self.safe:
            try:
                self.safe = self.safe.resolve(context)
            except AttributeError:
                self.safe = True

        if self.template:
            return self.render_as_template(context, snippet, default_text)
        if self.safe:
            return mark_safe(snippet)

        return conditional_escape(snippet)
