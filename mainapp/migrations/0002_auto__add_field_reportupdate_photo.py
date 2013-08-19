# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'ReportUpdate.photo'
        db.add_column(u'report_updates', 'photo', self.gf('stdimage.fields.StdImageField')(blank=True, default='', max_length=100, thumbnail_size={'width': 133, 'force': None, 'height': 100}, size={'width': 200, 'force': None, 'height': 200}), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'ReportUpdate.photo'
        db.delete_column(u'report_updates', 'photo')


    models = {
        'mainapp.city': {
            'Meta': {'object_name': 'City', 'db_table': "u'cities'"},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mainapp.Province']"})
        },
        'mainapp.councillor': {
            'Meta': {'object_name': 'Councillor', 'db_table': "u'councillors'"},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'first_name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'mainapp.emailrule': {
            'Meta': {'object_name': 'EmailRule'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mainapp.ReportCategory']", 'null': 'True', 'blank': 'True'}),
            'category_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mainapp.ReportCategoryClass']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mainapp.City']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_cc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rule': ('django.db.models.fields.IntegerField', [], {})
        },
        'mainapp.faqentry': {
            'Meta': {'object_name': 'FaqEntry', 'db_table': "u'faq_entries'"},
            'a_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'a_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'q_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'q_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'mainapp.pollingstation': {
            'Meta': {'object_name': 'PollingStation', 'db_table': "u'polling_stations'"},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mainapp.City']"}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'ward_number': ('django.db.models.fields.IntegerField', [], {})
        },
        'mainapp.province': {
            'Meta': {'object_name': 'Province', 'db_table': "u'province'"},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mainapp.report': {
            'Meta': {'object_name': 'Report', 'db_table': "u'reports'"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mainapp.ReportCategory']", 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email_sent_to': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'fixed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_fixed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_hate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo': ('stdimage.fields.StdImageField', [], {'blank': 'True', 'max_length': '100', 'thumbnail_size': "{'width': 133, 'force': None, 'height': 100}", 'size': "{'width': 400, 'force': None, 'height': 400}"}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'reminded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ward': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mainapp.Ward']", 'null': 'True'})
        },
        'mainapp.reportcategory': {
            'Meta': {'object_name': 'ReportCategory', 'db_table': "u'report_categories'"},
            'category_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mainapp.ReportCategoryClass']"}),
            'hint_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hint_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mainapp.reportcategoryclass': {
            'Meta': {'object_name': 'ReportCategoryClass', 'db_table': "u'report_category_classes'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mainapp.reportsubscriber': {
            'Meta': {'object_name': 'ReportSubscriber', 'db_table': "u'report_subscribers'"},
            'confirm_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mainapp.Report']"})
        },
        'mainapp.reportupdate': {
            'Meta': {'object_name': 'ReportUpdate', 'db_table': "u'report_updates'"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'confirm_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'first_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_fixed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('stdimage.fields.StdImageField', [], {'blank': 'True', 'max_length': '100', 'thumbnail_size': "{'width': 133, 'force': None, 'height': 100}", 'size': "{'width': 200, 'force': None, 'height': 200}"}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mainapp.Report']"})
        },
        'mainapp.verifiedauthor': {
            'Meta': {'object_name': 'VerifiedAuthor'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mainapp.ward': {
            'Meta': {'object_name': 'Ward', 'db_table': "u'wards'"},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mainapp.City']"}),
            'councillor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mainapp.Councillor']"}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['mainapp']