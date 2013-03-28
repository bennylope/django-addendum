from django.test import TestCase
from django.template import Context, Template

from .models import Snippet


class TagTests(TestCase):
    """
    Tests that the template tag renders the correct text
    """

    def setUp(self):
        self.plain_snippet = Snippet.objects.create(id="plain",
                text="Hello, humans")
        self.rich_snippet = Snippet.objects.create(id="rich",
                text="<h1>Hello, humans</h1>")

    def test_has_snippet(self):
        """Ensure that the saved snippet text is displayed"""
        t = Template("""{% spaceless %}{% load addendum_tags %}{% snippet 'plain' %}Hello world{% endsnippet %}{% endspaceless %}""")
        c = Context({})
        result = t.render(c)
        self.assertEqual(result, "Hello, humans")

    def test_no_snippet(self):
        """Ensure that the default text is displayed"""
        t = Template("""{% spaceless %}{% load addendum_tags %}{% snippet 'missing' %}Hello world{% endsnippet %}{% endspaceless %}""")
        c = Context({})
        result = t.render(c)
        self.assertEqual(result, "Hello world")

    def test_plain_text(self):
        """Ensure that content is not escaped"""
        t = Template("""{% spaceless %}{% load addendum_tags %}{% snippet 'rich' %}Hello world{% endsnippet %}{% endspaceless %}""")
        c = Context({})
        result = t.render(c)
        self.assertEqual(result, "&lt;h1&gt;Hello, humans&lt;/h1&gt;")

    def test_richtext(self):
        """Ensure that with richtext argument content is escaped"""
        t = Template("""{% spaceless %}{% load addendum_tags %}{% snippet 'rich' richtext=True %}Hello world{% endsnippet %}{% endspaceless %}""")
        c = Context({})
        result = t.render(c)
        self.assertEqual(result, "<h1>Hello, humans</h1>")
