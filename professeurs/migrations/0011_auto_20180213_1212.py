# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-13 12:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('professeurs', '0010_auto_20180213_1110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rapportblocusjournalier',
            old_name='productivité',
            new_name='productivite',
        ),
    ]
