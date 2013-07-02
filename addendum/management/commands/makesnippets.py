import os
import re
import codecs

from django.core.management.base import BaseCommand
from django.template import Template
from django.conf import settings

from addendum.models import Snippet
from addendum.templatetags.addendum_tags import SnippetNode
from django.template.loaders.app_directories import app_template_dirs


IS_ADDENDUM = r'\{\% load addendum_tags \%\}'


def get_addendum_templates():
    for template in get_all_templates():
        try:
            with codecs.open(template, 'r',
                             settings.DEFAULT_CHARSET) as template:
                yield template.read()
        except UnicodeDecodeError:
            pass


def is_addendum(template_string):
    """Checks if the template_string loads the addendum tags"""
    return re.search(IS_ADDENDUM, template_string)


def _get_nodes(template):
    return template.nodelist.get_nodes_by_type(SnippetNode)


def get_all_templates():
    for template_dir in (settings.TEMPLATE_DIRS + app_template_dirs):
        for dir, dirnames, filenames in os.walk(template_dir):
            for filename in filenames:
                yield os.path.join(dir, filename)


def search_snippet_nodes(template_string):
    """
    Given a valid django template string,
    compiles it and extracts all SnippetNode nodes
    """
    t = Template(template_string)
    return [node for node in _get_nodes(t)]


class Command(BaseCommand):
    help = 'Creates snippet instances from templates'

    def __init__(self, *args, **kwargs):
        self.found = []  # list for storing re.matches
        super(Command, self).__init__(*args, **kwargs)

    def search_files(self):
        for data in get_addendum_templates():
            # check if the template loads addendum
            if is_addendum(data):
                snippets = search_snippet_nodes(data)
                self.parse_snippets(snippets)

    def parse_snippets(self, snippets):
        for s in snippets:
            self.found.append({'name': s.key.literal, 'content': s.render({})})

    def handle_results(self):
        for snip in self.found:
            snip, created = Snippet.objects.get_or_create(
                key=snip['name'],
                defaults={'text': snip['content']}
            )
            print("Snippet found: {}".format(snip.key))

    def handle(self, *args, **options):
        self.search_files()
        self.handle_results()
