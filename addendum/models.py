#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import warnings

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


def set_cached_snippet(key):
    """
    Adds a dictionary of snippet text and translations to the cache.

    The default text has the key of an empty string.

        {
            "": "Hello, humans",
            "es": "Hola, humanos",
            "en-au": "G'day, humans",
        }

    """
    text_dict = {
        trans.language: trans.text for trans in
        SnippetTranslation.objects.filter(snippet_id=key)
    }
    text_dict.update({'': Snippet.objects.get(key=key).text})
    cache.set('snippet:{0}'.format(key), text_dict)


def get_cached_snippet(key, language=''):
    """
    Fetches the snippet from cache.

    Returns the text value (string) of a Snippet or None.

    This method addes every queried key to the cache to ensure that misses
    doesn't continue to generate database lookups. Since `None` is the
    default return value for a cache miss, the method uses -1 as the miss
    value. If this is returned we know that the value should not be present
    in the database, either.

    :param key: the snippet key (string)
    :param language: optional language code (string)
    :returns: text of snippet (string) or None
    """
    # TODO on fallback try looking for parent language string, e.g. if 'es-ar'
    # is missing then try looking for 'es'.

    snippet = cache.get('snippet:{0}'.format(key))

    # Previous cache miss and DB miss
    if snippet == -1:
        return None

    # First cache miss
    if snippet is None:
        try:
            snippet = Snippet.objects.get(key=key)
        except Snippet.DoesNotExist:
            cache.set('snippet:{0}'.format(key), -1)
            snippet = {'': None}
        else:
            set_cached_snippet(key)
            snippet = cache.get('snippet:{0}'.format(key))

    return snippet.get(language, snippet.get(''))


class CachedManager(models.Manager):

    def get_from_cache(self, key):
        """
        DEPRECATED.

        Use get_cached_snippet instead.
        """
        warnings.warn("The CachedManager is now deprecated, use get_cached_text instead",
                DeprecationWarning)
        snippet = cache.get('snippet:{0}'.format(key))

        if snippet == -1:
            return None

        if snippet is None:
            try:
                snippet = Snippet.objects.get(key=key)
            except Snippet.DoesNotExist:
                cache.set('snippet:{0}'.format(key), -1)
            else:
                cache.set('snippet:{0}'.format(key), snippet)

        return snippet


class Snippet(models.Model):
    """
    Model for storing snippets of text for replacement in templates.

    This should be used for the default language in the case of a multilingual
    app.
    """
    key = models.CharField(max_length=250, primary_key=True)
    text = models.TextField()
    objects = CachedManager()

    class Meta:
        ordering = ('key',)

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        super(Snippet, self).save(*args, **kwargs)
        set_cached_snippet(self.key)
        return self


@receiver(post_delete, sender=Snippet)
def delete_snippet(instance, **kwargs):
    cache.delete('snippet:{0}'.format(instance.key))


class SnippetTranslation(models.Model):
    """
    Additional text copies of the original snippet for use with the specified
    language.
    """
    snippet = models.ForeignKey(Snippet, related_name="translations")
    language = models.CharField(max_length=5)
    text = models.TextField()

    class Meta:
        unique_together = ('snippet', 'language')

    def __str__(self):
        return "{0} ({1})".format(self.snippet, self.language)

    def save(self, *args, **kwargs):
        super(SnippetTranslation, self).save(*args, **kwargs)
        set_cached_snippet(self.snippet_id)
        return self


@receiver(post_delete, sender=SnippetTranslation)
def delete_snippet_translation(instance, **kwargs):
    """
    After removing from the database update the snippet cache values.
    """
    set_cached_snippet(instance.snippet_id)
