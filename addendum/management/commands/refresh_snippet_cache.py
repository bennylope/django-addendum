"""
Management command to update all snippet cached values.
"""

from django.core.management.base import BaseCommand

from ...models import SnippetTranslation, Snippet


class Command(BaseCommand):
    help = "Updates the cache values for all snippets including translations"

    def handle(self, *args, **kwargs):
        snippet_count, translation_count = 0, 0
        for snippet in Snippet.objects.all():
            snippet.set_cache()
            snippet_count += 1
        for snippet in SnippetTranslation.objects.all():
            snippet.set_cache()
            translation_count += 1
        self.stdout.write(
                "Refreshed the cache for {0} snippets and {1} translations".format(
                    snippet_count, translation_count))
