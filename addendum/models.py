import warnings

from django.conf import settings
from django.core.cache import cache
from django.db import models


def get_cached_snippet(key):
    """
    Fetches the snippet from cache.

    Returns the text value (string) of a Snippet or None.

    This method addes every queried key to the cache to ensure that misses
    doesn't continue to generate database lookups. Since `None` is the
    default return value for a cache miss, the method uses -1 as the miss
    value. If this is returned we know that the value should not be present
    in the database, either.
    """
    text = cache.get('snippet:{0}'.format(key))

    if text == -1:
        return None

    if text is None:
        try:
            text = Snippet.objects.get(key=key).text
        except Snippet.DoesNotExist:
            cache.set('snippet:{0}'.format(key), -1)
        else:
            cache.set('snippet:{0}'.format(key), text)

    return text


def get_cached_translation(key, language):
    """
    Returns a snippet by given language, defaulting to the base snippet if
    unavailable.
    """
    text = cache.get('snippet:{0}:{1}'.format(language, key))

    if text == -1:
        return None

    if text is None:
        try:
            text = SnippetTranslation.objects.get(snippet_id=key, language=language).text
        except SnippetTranslation.DoesNotExist:
            cache.set('snippet:{0}:{1}'.format(language, key), -1)
            text = get_cached_snippet(key)

    return text


def get_cached_text(key, language=None):
    """
    Interface function for getting the text of a snippet by key and/or by
    language.
    """
    if language is not None:
        return get_cached_translation(key, language)
    return get_cached_snippet(key)


class CachedManager(models.Manager):

    def get_from_cache(self, key):
        """
        Fetches the snippet from cache.

        Returns a `Snippet` object or `None`.

        This method addes every queried key to the cache to ensure that misses
        doesn't continue to generate database lookups. Since `None` is the
        default return value for a cache miss, the method uses -1 as the miss
        value. If this is returned we know that the value should not be present
        in the database, either.
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
        self.set_cache()
        return self

    def delete(self, **kwargs):
        cache.delete('snippet:{0}'.format(self.key))
        return super(Snippet, self).delete(**kwargs)

    def set_cache(self):
        """
        Updates the cached value of the instance
        """
        cache.set('snippet:{0}'.format(self.key), self.text)


class SnippetTranslation(models.Model):
    """
    Additional text copies of the original snippet for use with the specified
    language.
    """
    snippet = models.ForeignKey(Snippet, related_name="translations")
    language = models.CharField(max_length=5, choices=settings.LANGUAGES)
    text = models.TextField()

    class Meta:
        unique_together = ('snippet', 'language')

    def __str__(self):
        return "{0} ({1})".format(self.snippet, self.language)

    def save(self, *args, **kwargs):
        super(SnippetTranslation, self).save(*args, **kwargs)
        self.set_cache()
        return self

    def delete(self, **kwargs):
        cache.delete('snippet:{0}:{1}'.format(self.language, self.snippet))
        return super(Snippet, self).delete(**kwargs)

    def set_cache(self):
        """
        Updates the cached value of the instance
        """
        cache.set('snippet:{0}:{1}'.format(self.language, self.snippet), self.text)
