# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SnippetTranslation'
        db.create_table(u'addendum_snippettranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('snippet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['addendum.Snippet'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'addendum', ['SnippetTranslation'])

        # Adding unique constraint on 'SnippetTranslation', fields ['snippet', 'language']
        db.create_unique(u'addendum_snippettranslation', ['snippet_id', 'language'])


    def backwards(self, orm):
        # Removing unique constraint on 'SnippetTranslation', fields ['snippet', 'language']
        db.delete_unique(u'addendum_snippettranslation', ['snippet_id', 'language'])

        # Deleting model 'SnippetTranslation'
        db.delete_table(u'addendum_snippettranslation')


    models = {
        u'addendum.snippet': {
            'Meta': {'ordering': "('key',)", 'object_name': 'Snippet'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '250', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'addendum.snippettranslation': {
            'Meta': {'unique_together': "(('snippet', 'language'),)", 'object_name': 'SnippetTranslation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': u"orm['addendum.Snippet']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['addendum']