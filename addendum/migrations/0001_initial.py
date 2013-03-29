# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Snippet'
        db.create_table(u'addendum_snippet', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'addendum', ['Snippet'])


    def backwards(self, orm):
        # Deleting model 'Snippet'
        db.delete_table(u'addendum_snippet')


    models = {
        u'addendum.snippet': {
            'Meta': {'ordering': "('key',)", 'object_name': 'Snippet'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['addendum']