# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Snippet.id'
        db.delete_column(u'addendum_snippet', 'id')


        # Changing field 'Snippet.key'
        db.alter_column(u'addendum_snippet', 'key', self.gf('django.db.models.fields.CharField')(default=1, max_length=100, primary_key=True))
        # Adding unique constraint on 'Snippet', fields ['key']
        db.create_unique(u'addendum_snippet', ['key'])


    def backwards(self, orm):
        # Removing unique constraint on 'Snippet', fields ['key']
        db.delete_unique(u'addendum_snippet', ['key'])


        # User chose to not deal with backwards NULL issues for 'Snippet.id'
        raise RuntimeError("Cannot reverse this migration. 'Snippet.id' and its values cannot be restored.")

        # Changing field 'Snippet.key'
        db.alter_column(u'addendum_snippet', 'key', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    models = {
        u'addendum.snippet': {
            'Meta': {'ordering': "('key',)", 'object_name': 'Snippet'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['addendum']