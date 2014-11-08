# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Snippet.key'
        db.alter_column('addendum_snippet', 'key', self.gf('django.db.models.fields.CharField')(max_length=250, primary_key=True))

    def backwards(self, orm):

        # Changing field 'Snippet.key'
        db.alter_column('addendum_snippet', 'key', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True))

    models = {
        'addendum.snippet': {
            'Meta': {'ordering': "('key',)", 'object_name': 'Snippet'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '250', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['addendum']