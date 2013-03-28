from django.db import models


class Snippet(models.Model):
    """
    Model for storing snippets of text for replacement in templates
    """
    id = models.CharField(max_length=100, primary_key=True)
    text = models.TextField()

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return self.id
