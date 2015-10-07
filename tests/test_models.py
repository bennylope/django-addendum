# encoding: utf-8

from __future__ import unicode_literals

from django.test import TestCase

from addendum.models import Snippet


class ModelTests(TestCase):

    def test_unicode(self):
        s = Snippet.objects.create(key="holá", text="World")
        self.assertEqual(s.__str__(), "holá")
