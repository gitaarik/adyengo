# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Session'
        db.create_table(u'adyen_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('merchant_reference', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('payment_amount', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('currency_code', self.gf('django.db.models.fields.CharField')(default=None, max_length=3)),
            ('ship_before_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('skin_code', self.gf('django.db.models.fields.CharField')(default='Nl0r8s5C', max_length=10)),
            ('shopper_locale', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('order_data', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('session_validity', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('merchant_return_data', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('shopper_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('shopper_reference', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('shopper_ip', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('shopper_statement', self.gf('django.db.models.fields.CharField')(max_length=135, blank=True)),
            ('fraud_offset', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('recurring_contract', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('recurring_detail_reference', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('page_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'adyen', ['Session'])

        # Adding model 'SessionAllowedPaymentMethods'
        db.create_table(u'adyen_sessionallowedpaymentmethods', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(related_name='allowed_payment_methods', to=orm['adyen.Session'])),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'adyen', ['SessionAllowedPaymentMethods'])

        # Adding model 'SessionBlockedPaymentMethods'
        db.create_table(u'adyen_sessionblockedpaymentmethods', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(related_name='blocked_payment_methods', to=orm['adyen.Session'])),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'adyen', ['SessionBlockedPaymentMethods'])

        # Adding model 'RecurringContract'
        db.create_table(u'adyen_recurringcontract', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shopper_reference', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('contract_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('recurring_detail_reference', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('variant', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('payment_method_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'adyen', ['RecurringContract'])

        # Adding model 'RecurringContractDetail'
        db.create_table(u'adyen_recurringcontractdetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recurring_contract', self.gf('django.db.models.fields.related.ForeignKey')(related_name='details', to=orm['adyen.RecurringContract'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal(u'adyen', ['RecurringContractDetail'])

        # Adding model 'RecurringPaymentResult'
        db.create_table(u'adyen_recurringpaymentresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recurring_payment_results', to=orm['adyen.Session'])),
            ('psp_reference', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=20)),
            ('result_code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('auth_code', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('refusal_reason', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal(u'adyen', ['RecurringPaymentResult'])

        # Adding model 'Notification'
        db.create_table(u'adyen_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('live', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('event_code', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('psp_reference', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('original_reference', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('merchant_reference', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('merchant_account_code', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('event_date', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('payment_method', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('operations', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('valid', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adyen.Session'], null=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'adyen', ['Notification'])

        # Adding unique constraint on 'Notification', fields ['live', 'psp_reference', 'event_code']
        db.create_unique(u'adyen_notification', ['live', 'psp_reference', 'event_code'])


    def backwards(self, orm):
        # Removing unique constraint on 'Notification', fields ['live', 'psp_reference', 'event_code']
        db.delete_unique(u'adyen_notification', ['live', 'psp_reference', 'event_code'])

        # Deleting model 'Session'
        db.delete_table(u'adyen_session')

        # Deleting model 'SessionAllowedPaymentMethods'
        db.delete_table(u'adyen_sessionallowedpaymentmethods')

        # Deleting model 'SessionBlockedPaymentMethods'
        db.delete_table(u'adyen_sessionblockedpaymentmethods')

        # Deleting model 'RecurringContract'
        db.delete_table(u'adyen_recurringcontract')

        # Deleting model 'RecurringContractDetail'
        db.delete_table(u'adyen_recurringcontractdetail')

        # Deleting model 'RecurringPaymentResult'
        db.delete_table(u'adyen_recurringpaymentresult')

        # Deleting model 'Notification'
        db.delete_table(u'adyen_notification')


    models = {
        u'adyen.notification': {
            'Meta': {'ordering': "('-creation_time',)", 'unique_together': "(('live', 'psp_reference', 'event_code'),)", 'object_name': 'Notification'},
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'merchant_account_code': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'merchant_reference': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'operations': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'original_reference': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'psp_reference': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adyen.Session']", 'null': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'adyen.recurringcontract': {
            'Meta': {'ordering': "('-creation_time',)", 'object_name': 'RecurringContract'},
            'contract_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_method_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'recurring_detail_reference': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'shopper_reference': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'variant': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'adyen.recurringcontractdetail': {
            'Meta': {'object_name': 'RecurringContractDetail'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'recurring_contract': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'details'", 'to': u"orm['adyen.RecurringContract']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        u'adyen.recurringpaymentresult': {
            'Meta': {'object_name': 'RecurringPaymentResult'},
            'auth_code': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'psp_reference': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '20'}),
            'refusal_reason': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'result_code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recurring_payment_results'", 'to': u"orm['adyen.Session']"})
        },
        u'adyen.session': {
            'Meta': {'ordering': "('-creation_time',)", 'object_name': 'Session'},
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '3'}),
            'fraud_offset': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant_reference': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'merchant_return_data': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'order_data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'payment_amount': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'recurring_contract': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'recurring_detail_reference': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'session_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'session_validity': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'ship_before_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'shopper_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'shopper_ip': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'shopper_locale': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'shopper_reference': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'shopper_statement': ('django.db.models.fields.CharField', [], {'max_length': '135', 'blank': 'True'}),
            'skin_code': ('django.db.models.fields.CharField', [], {'default': "'Nl0r8s5C'", 'max_length': '10'})
        },
        u'adyen.sessionallowedpaymentmethods': {
            'Meta': {'object_name': 'SessionAllowedPaymentMethods'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'allowed_payment_methods'", 'to': u"orm['adyen.Session']"})
        },
        u'adyen.sessionblockedpaymentmethods': {
            'Meta': {'object_name': 'SessionBlockedPaymentMethods'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blocked_payment_methods'", 'to': u"orm['adyen.Session']"})
        }
    }

    complete_apps = ['adyen']