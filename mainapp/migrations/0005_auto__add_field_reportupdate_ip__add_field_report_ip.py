# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ReportUpdate.ip'
        db.add_column(u'report_updates', 'ip',
                      self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True),
                      keep_default=False)

        # Adding field 'Report.ip'
        db.add_column(u'reports', 'ip',
                      self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ReportUpdate.ip'
        db.delete_column(u'report_updates', 'ip')

        # Deleting field 'Report.ip'
        db.delete_column(u'reports', 'ip')


    models = {
        u'mainapp.city': {
            'Meta': {'object_name': 'City', 'db_table': "u'cities'"},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Province']"})
        },
        u'mainapp.councillor': {
            'Meta': {'object_name': 'Councillor', 'db_table': "u'councillors'"},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'first_name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'mainapp.emailrule': {
            'Meta': {'object_name': 'EmailRule'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.ReportCategory']", 'null': 'True', 'blank': 'True'}),
            'category_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.ReportCategoryClass']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.City']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_cc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rule': ('django.db.models.fields.IntegerField', [], {})
        },
        u'mainapp.faqentry': {
            'Meta': {'object_name': 'FaqEntry', 'db_table': "u'faq_entries'"},
            'a_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'a_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'q_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'q_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'mainapp.pollingstation': {
            'Meta': {'object_name': 'PollingStation', 'db_table': "u'polling_stations'"},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.City']"}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'ward_number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'mainapp.province': {
            'Meta': {'object_name': 'Province', 'db_table': "u'province'"},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mainapp.report': {
            'Meta': {'object_name': 'Report', 'db_table': "u'reports'"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.ReportCategory']", 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email_sent_to': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'fixed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_fixed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_hate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo': ('stdimage.fields.StdImageField', [], {'max_length': '100', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'reminded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ward': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Ward']", 'null': 'True'})
        },
        u'mainapp.reportcategory': {
            'Meta': {'object_name': 'ReportCategory', 'db_table': "u'report_categories'"},
            'category_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.ReportCategoryClass']"}),
            'hint_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hint_ka': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mainapp.reportcategoryclass': {
            'Meta': {'object_name': 'ReportCategoryClass', 'db_table': "u'report_category_classes'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mainapp.reportsubscriber': {
            'Meta': {'object_name': 'ReportSubscriber', 'db_table': "u'report_subscribers'"},
            'confirm_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Report']"})
        },
        u'mainapp.reportupdate': {
            'Meta': {'object_name': 'ReportUpdate', 'db_table': "u'report_updates'"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'confirm_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'first_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_fixed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('stdimage.fields.StdImageField', [], {'max_length': '100', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Report']"})
        },
        u'mainapp.verifiedauthor': {
            'Meta': {'object_name': 'VerifiedAuthor'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'mainapp.ward': {
            'Meta': {'object_name': 'Ward', 'db_table': "u'wards'"},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.City']"}),
            'councillor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mainapp.Councillor']"}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ka': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['mainapp']