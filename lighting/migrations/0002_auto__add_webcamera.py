# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WebCamera'
        db.create_table('lighting_webcamera', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('motion_control', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('lighting', ['WebCamera'])


    def backwards(self, orm):
        # Deleting model 'WebCamera'
        db.delete_table('lighting_webcamera')


    models = {
        'lighting.lighter': {
            'Meta': {'object_name': 'Lighter'},
            'access_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_type': ('django.db.models.fields.IntegerField', [], {}),
            'lighter_type': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'lighting.rule': {
            'Meta': {'object_name': 'Rule'},
            'end': ('django.db.models.fields.TimeField', [], {}),
            'end_delta': ('django.db.models.fields.IntegerField', [], {}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lighter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lighting.Lighter']"}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'start_delta': ('django.db.models.fields.IntegerField', [], {}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'lighting.webcamera': {
            'Meta': {'object_name': 'WebCamera'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motion_control': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'lighting.zwaveapi': {
            'Meta': {'object_name': 'ZWaveApi'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['lighting']