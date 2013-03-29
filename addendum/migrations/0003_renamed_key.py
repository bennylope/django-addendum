# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.db import connection, transaction

class Migration(DataMigration):

    def forwards(self, orm):
        cursor = connection.cursor()
        cursor.execute("UPDATE addendum_snippet SET key=id;")
        transaction.commit_unless_managed()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        u'addendum.snippet': {
            'Meta': {'ordering': "('key',)", 'object_name': 'Snippet'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['addendum']
    symmetrical = True
