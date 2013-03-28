from django import template
from django.template.base import TemplateSyntaxError, kwarg_re
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from ..models import Snippet


register = template.Library()


@register.tag
def snippet(parser, token):
    """
    """
    nodelist = parser.parse(('endsnippet',))
    parser.delete_first_token()

    try:
        # split_contents() knows not to split quoted strings.
        tag_name, key, rich = token.split_contents()
        try:
            richkey, richval = rich.split('=')
        except ValueError:
            raise TemplateSyntaxError("Bad or badly formed richtext kwargs")
        else:
            if richkey != 'richtext':
                raise TemplateSyntaxError("Bad or badly formed richtext kwargs")
            richtext = True if richval == 'True' else False

    except ValueError:
        tag_name, key = token.split_contents()
        richtext = False
    return SnippetNode(nodelist, key[1:-1], richtext)


class SnippetNode(template.Node):

    def __init__(self, nodelist, key, richtext=False):
        self.nodelist = nodelist
        self.key = key
        self.richtext = richtext

    def render(self, context):
        key = self.key
        try:
            snippet = Snippet.objects.get_from_cache(id=key)
        except Snippet.DoesNotExist:
            output = self.nodelist.render(context)
            return output

        if self.richtext:
            return mark_safe(snippet.text)
        return conditional_escape(snippet.text)
