from django.contrib import admin
from django.conf import settings

from .forms import TranslationForm
from .models import Snippet, SnippetTranslation


class TranslationAdmin(admin.TabularInline):
    model = SnippetTranslation
    form = TranslationForm
    extra = 0


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('key', 'text')
    inlines = [TranslationAdmin]

    def __init__(self, *args, **kwargs):
        """
        Hides the translation inlines if the project does not have i18n
        enabled.
        """
        if not settings.USE_I18N:
            self.inlines = []
        super(SnippetAdmin, self).__init__(*args, **kwargs)


admin.site.register(Snippet, SnippetAdmin)
