from django.contrib import admin

from .models import Snippet


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')


admin.site.register(Snippet, SnippetAdmin)
