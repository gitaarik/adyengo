# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Notification', fields ['live', 'event_code', 'psp_reference']
        db.delete_unique(u'adyen_notification', ['live', 'event_code', 'psp_reference'])

        # Adding unique constraint on 'Notification', fields ['live', 'event_code', 'merchant_account_code', 'psp_reference']
        db.create_unique(u'adyen_notification', ['live', 'event_code', 'merchant_account_code', 'psp_reference'])


    def backwards(self, orm):
        # Removing unique constraint on 'Notification', fields ['live', 'event_code', 'merchant_account_code', 'psp_reference']
        db.delete_unique(u'adyen_notification', ['live', 'event_code', 'merchant_account_code', 'psp_reference'])

        # Adding unique constraint on 'Notification', fields ['live', 'event_code', 'psp_reference']
        db.create_unique(u'adyen_notification', ['live', 'event_code', 'psp_reference'])


    models = {
        u'adyen.notification': {
            'Meta': {'ordering': "('-creation_time',)", 'unique_together': "(('live', 'merchant_account_code', 'psp_reference', 'event_code'),)", 'object_name': 'Notification'},
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