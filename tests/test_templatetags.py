# encoding: utf-8

from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import RequestFactory
from django.template import Context, RequestContext, Template

from addendum.models import Snippet, SnippetTranslation


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
        SnippetTranslation.objects.create(
            snippet=self.plain_snippet,
            language='es',
            text="Hola, humanos",
        )
        SnippetTranslation.objects.create(
            snippet=self.plain_snippet,
            language='en-au',
            text="G'day, humans",
        )

    def test_has_snippet(self):
        """Ensure that the saved snippet text is displayed"""
        t = Template("""{% load addendum_tags %}{% snippet 'plain' %}Hello world{% endsnippet %}""")
        c = Context({})
        result = t.render(c)
        self.assertEqual(result, "Hello, humans")

    def test_no_snippet(self):
        """Ensure that the default text is displayed"""
        t = Template("""{% load addendum_tags %}{% snippet 'missing' %}Hello world{% endsnippet %}""")
        c = Context({})
        result = t.render(c)
        self.assertEqual(result, "Hello world")

    def test_plain_text(self):
        """Ensure that content is not escaped"""
        t = Template("""{% load addendum_tags %}{% snippet 'rich' %}Hello world{% endsnippet %}""")
        c = Context({})
        result = t.render(c)
        self.assertEqual(result, "&lt;h1&gt;Hello, humans&lt;/h1&gt;")

    def test_richtext(self):
        """Ensure that with richtext argument content is escaped"""
        t = Template("""{% load addendum_tags %}{% snippet 'rich' richtext=True %}Hello world{% endsnippet %}""")
        c = Context({})
        result = t.render(c)
        self.assertEqual(result, "<h1>Hello, humans</h1>")

    def test_safe(self):
        """Ensure that with safe argument content is escaped"""
        t = Template("""{% load addendum_tags %}{% snippet 'rich' safe=True %}Hello world{% endsnippet %}""")
        c = Context({})
        result = t.render(c)
        self.assertEqual(result, "<h1>Hello, humans</h1>")

    def test_safe_false(self):
        """Ensure that with safe argument which is False content is not escaped"""
        t = Template("""{% load addendum_tags %}{% snippet 'rich' safe=isallowed %}Hello world{% endsnippet %}""")
        c = Context({'isallowed': False})
        result = t.render(c)
        self.assertEqual(result, "&lt;h1&gt;Hello, humans&lt;/h1&gt;")

    def test_raw_template_text(self):
        """Ensure template code is not compiled by default"""
        t = Template("""{% load addendum_tags %}{% snippet 'django' %}Hello world{% endsnippet %}""")
        c = Context({'dog': 'woof'})
        result = t.render(c)
        self.assertEqual(result, "{{ dog|upper }}")

    def test_template_text(self):
        """Ensure template code is rendered with the template option"""
        t = Template("""{% load addendum_tags %}{% snippet 'django' template=True %}Hello world{% endsnippet %}""")
        c = Context({'dog': 'woof'})
        result = t.render(c)
        self.assertEqual(result, "WOOF")

    def test_safe_template_text(self):
        t = Template("""{% load addendum_tags %}{% snippet 'django' template=True %}Hello world{% endsnippet %}""")
        c = Context({'dog': '<h1>woof</h1>'})
        result = t.render(c)
        self.assertEqual(result, "&lt;H1&gt;WOOF&lt;/H1&gt;")

        t = Template("""{% load addendum_tags %}{% snippet 'django' template=True safe=True %}Hello world{% endsnippet %} {{ after }}""")
        c = Context({'dog': '<h1>woof</h1>', 'after': '<h1>no longer safe</h1>'})
        result = t.render(c)
        self.assertEqual(result, "<H1>WOOF</H1> &lt;h1&gt;no longer safe&lt;/h1&gt;")

    def test_variable_key_name(self):
        """Ensure a variable can be passed for the snippet key"""
        t = Template("""{% load addendum_tags %}{% snippet snippetname %}Hello world{% endsnippet %}""")
        c = Context({'snippetname': 'plain'})
        result = t.render(c)
        self.assertEqual(result, "Hello, humans")

    def test_translate_basic(self):
        """Translate based on passed language code"""
        t = Template("""{% load addendum_tags %}{% snippet 'plain' language='es' %}Hello world{% endsnippet %}""")
        c = Context({})
        result = t.render(c)
        self.assertEqual(result, "Hola, humanos")

    def test_missing_translation(self):
        """Return default language for missing translation"""
        t = Template("""{% load addendum_tags %}{% snippet 'plain' language='es-mx' %}Hello world{% endsnippet %}""")
        c = Context({})
        result = t.render(c)
        self.assertEqual(result, "Hello, humans")

    def test_specified_language(self):
        """Ensure specified language is used, not default"""
        t = Template("""{% load addendum_tags %}{% snippet 'plain' language=lang safe=True %}Hello world{% endsnippet %}""")
        c = Context({'lang': 'en-au'})
        result = t.render(c)
        self.assertEqual(result, "G'day, humans")

    def test_no_specified_language(self):
        """Ensure that the current site language is used"""
        request = RequestFactory().request()
        t = Template("""{% load addendum_tags %}{% snippet 'plain' %}Hello world{% endsnippet %}""")
        c = RequestContext(request, {})
        result = t.render(c)
        self.assertEqual(result, "Hola, humanos")
