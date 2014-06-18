# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ZWaveApi'
        db.create_table('lighting_zwaveapi', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('lighting', ['ZWaveApi'])

        # Adding model 'Lighter'
        db.create_table('lighting_lighter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('access_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lighter_type', self.gf('django.db.models.fields.IntegerField')()),
            ('internal_type', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('lighting', ['Lighter'])

        # Adding model 'Rule'
        db.create_table('lighting_rule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lighter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lighting.Lighter'])),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('start_delta', self.gf('django.db.models.fields.IntegerField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('end_delta', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('lighting', ['Rule'])


    def backwards(self, orm):
        # Deleting model 'ZWaveApi'
        db.delete_table('lighting_zwaveapi')

        # Deleting model 'Lighter'
        db.delete_table('lighting_lighter')

        # Deleting model 'Rule'
        db.delete_table('lighting_rule')


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
        'lighting.zwaveapi': {
            'Meta': {'object_name': 'ZWaveApi'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['lighting']