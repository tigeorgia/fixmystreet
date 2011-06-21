# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Province'
        db.create_table(u'province', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_ka', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('abbrev', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('mainapp', ['Province'])

        # Adding model 'City'
        db.create_table(u'cities', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainapp.Province'])),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_ka', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal('mainapp', ['City'])

        # Adding model 'Councillor'
        db.create_table(u'councillors', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('first_name_ka', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('last_name_ka', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('mainapp', ['Councillor'])

        # Adding model 'Ward'
        db.create_table(u'wards', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_ka', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('councillor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainapp.Councillor'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainapp.City'])),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True)),
        ))
        db.send_create_signal('mainapp', ['Ward'])

        # Adding model 'ReportCategoryClass'
        db.create_table(u'report_category_classes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_ka', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('mainapp', ['ReportCategoryClass'])

        # Adding model 'ReportCategory'
        db.create_table(u'report_categories', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_ka', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('hint_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('hint_ka', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('category_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainapp.ReportCategoryClass'])),
        ))
        db.send_create_signal('mainapp', ['ReportCategory'])

        # Adding model 'EmailRule'
        db.create_table('mainapp_emailrule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule', self.gf('django.db.models.fields.IntegerField')()),
            ('is_cc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainapp.City'])),
            ('category_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainapp.ReportCategoryClass'], null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainapp.ReportCategory'], null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal('mainapp', ['EmailRule'])

        # Adding model 'Report'
        db.create_table(u'reports', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainapp.ReportCategory'], null=True)),
            ('ward', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainapp.Ward'], null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fixed_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('is_fixed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_hate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('email_sent_to', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('reminded_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True)),
            ('photo', self.gf('contrib.stdimage.fields.StdImageField')(blank=True, max_length=100, thumbnail_size={'width': 133, 'force': None, 'height': 100}, size={'width': 400, 'force': None, 'height': 400})),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mainapp', ['Report'])

        # Adding model 'ReportUpdate'
        db.create_table(u'report_updates', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainapp.Report'])),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_fixed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_verified_author', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('confirm_token', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('first_update', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mainapp', ['ReportUpdate'])

        # Adding model 'ReportSubscriber'
        db.create_table(u'report_subscribers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainapp.Report'])),
            ('confirm_token', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('is_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('mainapp', ['ReportSubscriber'])

        # Adding model 'VerifiedAuthor'
        db.create_table('mainapp_verifiedauthor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mainapp', ['VerifiedAuthor'])

        # Adding model 'FaqEntry'
        db.create_table(u'faq_entries', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('q_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('q_ka', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('a_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('a_ka', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('mainapp', ['FaqEntry'])

        # Adding model 'PollingStation'
        db.create_table(u'polling_stations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('ward_number', self.gf('django.db.models.fields.IntegerField')()),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mainapp.City'])),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True)),
        ))
        db.send_create_signal('mainapp', ['PollingStation'])


    def backwards(self, orm):
        
        # Deleting model 'Province'
        db.delete_table(u'province')

        # Deleting model 'City'
        db.delete_table(u'cities')

        # Deleting model 'Councillor'
        db.delete_table(u'councillors')

        # Deleting model 'Ward'
        db.delete_table(u'wards')

        # Deleting model 'ReportCategoryClass'
        db.delete_table(u'report_category_classes')

        # Deleting model 'ReportCategory'
        db.delete_table(u'report_categories')

        # Deleting model 'EmailRule'
        db.delete_table('mainapp_emailrule')

        # Deleting model 'Report'
        db.delete_table(u'reports')

        # Deleting model 'ReportUpdate'
        db.delete_table(u'report_updates')

        # Deleting model 'ReportSubscriber'
        db.delete_table(u'report_subscribers')

        # Deleting model 'VerifiedAuthor'
        db.delete_table('mainapp_verifiedauthor')

        # Deleting model 'FaqEntry'
        db.delete_table(u'faq_entries')

        # Deleting model 'PollingStation'
        db.delete_table(u'polling_stations')


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
            'photo': ('contrib.stdimage.fields.StdImageField', [], {'blank': 'True', 'max_length': '100', 'thumbnail_size': "{'width': 133, 'force': None, 'height': 100}", 'size': "{'width': 400, 'force': None, 'height': 400}"}),
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
