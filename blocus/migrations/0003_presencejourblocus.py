# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-29 10:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ba2', '0001_initial'),
        ('blocus', '0002_moduleblocus'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresenceJourBlocus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('blocus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blocus.Blocus')),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ba2.Campus')),
            ],
        ),
    ]