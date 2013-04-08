from django.test import TestCase
from django.template import Context, Template

from .models import Snippet


class TagTests(TestCase):
    """
    Tests that the template tag renders the correct text
    """

    def setUp(self):
        self.plain_snippet = Snippet.objects.create(key="plain",
                text="Hello, humans")
        self.rich_snippet = Snippet.objects.create(key="rich",
                text="<h1>Hello, humans</h1>")
        self.template_snippet = Snippet.objects.create(key="django",
                text="{{ dog|upper }}")

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

    def test_raw_template_text(self):
        """Ensure template code is not compiled by default"""
        t = Template("""{% spaceless %}{% load addendum_tags %}{% snippet 'django' %}Hello world{% endsnippet %}{% endspaceless %}""")
        c = Context({'dog': 'woof'})
        result = t.render(c)
        self.assertEqual(result, "{{ dog|upper }}")

    def test_template_text(self):
        """Ensure template code is rendered with the template option"""
        t = Template("""{% spaceless %}{% load addendum_tags %}{% snippet 'django' template=True %}Hello world{% endsnippet %}{% endspaceless %}""")
        c = Context({'dog': 'woof'})
        result = t.render(c)
        self.assertEqual(result, "WOOF")

    def test_safe_template_text(self):
        t = Template("""{% spaceless %}{% load addendum_tags %}{% snippet 'django' template=True %}Hello world{% endsnippet %}{% endspaceless %}""")
        c = Context({'dog': '<h1>woof</h1>'})
        result = t.render(c)
        self.assertEqual(result, "&lt;H1&gt;WOOF&lt;/H1&gt;")

        t = Template("""{% spaceless %}{% load addendum_tags %}{% snippet 'django' template=True safe=True %}Hello world{% endsnippet %}{% endspaceless %}""")
        c = Context({'dog': '<h1>woof</h1>'})
        result = t.render(c)
        self.assertEqual(result, "<H1>WOOF</H1>")

    def test_variable_key_name(self):
        """Ensure a variable can be passed for the snippet key"""
        t = Template("""{% spaceless %}{% load addendum_tags %}{% snippet snippetname %}Hello world{% endsnippet %}{% endspaceless %}""")
        c = Context({'snippetname': 'plain'})
        result = t.render(c)
        self.assertEqual(result, "Hello, humans")
