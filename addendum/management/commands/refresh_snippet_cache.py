"""
Management command to update all snippet cached values.
"""

from django.core.management.base import BaseCommand

from ...models import set_cached_snippet, Snippet


class Command(BaseCommand):
    help = "Updates the cache values for all snippets"

    def handle(self, *args, **kwargs):
        # Already iterating, skip the extra count query
        count = 0
        for snippet in Snippet.objects.all():
            set_cached_snippet(snippet.key)
            count += 1
        self.stdout.write(
                "Refreshed the cache for {0} snippets.".format(count))
