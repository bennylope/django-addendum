# encoding: utf-8

from django import forms
from django.conf import settings

from .models import SnippetTranslation


class TranslationForm(forms.ModelForm):

    language = forms.ChoiceField(choices=settings.LANGUAGES)

    class Meta:
        model = SnippetTranslation
        fields = '__all__'
