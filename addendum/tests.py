from django.test import TestCase
from django.template import Context, Template

from .models import Snippet
from .templatetags.addendum_tags import SnippetNode
from .management.commands.makesnippets import is_addendum, search_snippet_nodes, Command


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


class MakeSnippetsTests(TestCase):
    """
    Tests that the makesnippets command creates missing snippets from templates
    """

    def test_is_addendum_positive_check(self):
        """
        A valid load addendum_tags tag should be
        considered as addendum template_string
        """
        template_string = """{% load addendum_tags %}"""
        check = is_addendum(template_string)
        self.assertTrue(check)

    def test_is_addendum_negative_check(self):
        """
        An invalid load addendum_tags tag shouldn't
        be considered as addendum template
        """
        template_string = """load addendum_tags"""
        check = is_addendum(template_string)
        self.assertFalse(check)

    def test_search_snippets_nodes(self):
        """
        Ensure that given a valid django template string,
        compiles it and extracts all SnippetNode nodes
        """
        template_string = """{% spaceless %}{% load addendum_tags %}{% snippet 'django' template=True safe=True %}Hello world{% endsnippet %}{% endspaceless %}"""
        nodes = search_snippet_nodes(template_string)
        self.assertEqual(len(nodes), 1)

    def test_search_empty_snippets_nodes(self):
        """
        Ensure that given a valid django template string,
        without any SnippetNodes, it doesn't extracts any node
        """
        template_string = """{% load addendum_tags %}"""
        nodes = search_snippet_nodes(template_string)
        self.assertEqual(len(nodes), 0)

    def test_parse_snippets(self):
        """
        Command.parse_snippets should populate the
        Command.found list collected snippet data
        """
        c = Command()
        assert len(c.found) == 0

        t = Template("""{% spaceless %}{% load addendum_tags %}{% snippet 'snippetname' %}Hello world{% endsnippet %}{% endspaceless %}""")
        snippet_nodes = t.nodelist.get_nodes_by_type(SnippetNode)
        c.parse_snippets(snippet_nodes)

        self.assertEqual(len(c.found), 1)
        self.assertEqual(c.found[0], {'name': 'snippetname', 'content': 'Hello world'})

    def test_handle_new_results(self):
        """Command.handle_results should save new snippets"""
        assert len(Snippet.objects.all()) == 0

        c = Command()
        c.found = [{'name': 'snippetname', 'content': 'Hello world'}]

        c.handle_results()

        snippets = Snippet.objects.all()
        self.assertEqual(len(snippets), 1)
        self.assertEqual(snippets[0].key, 'snippetname')
        self.assertEqual(snippets[0].text, 'Hello world')

    def test_handle_existing_results(self):
        """Command.handle_results should not save existing snippets"""
        assert len(Snippet.objects.all()) == 0
        Snippet.objects.create(key='snippetname', text='Hello World')

        c = Command()
        c.found = [{'name': 'snippetname', 'content': 'Hello world altered'}]

        c.handle_results()

        snippets = Snippet.objects.all()
        self.assertEqual(len(snippets), 1)
        self.assertEqual(snippets[0].key, 'snippetname')
        self.assertEqual(snippets[0].text, 'Hello World')
