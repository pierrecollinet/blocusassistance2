# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-22 08:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocus', '0002_auto_20180119_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presence',
            name='etudiant',
        ),
        migrations.RemoveField(
            model_name='presence',
            name='inscription',
        ),
        migrations.RemoveField(
            model_name='presence',
            name='jourblocus',
        ),
        migrations.DeleteModel(
            name='Presence',
        ),
    ]
