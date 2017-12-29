# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-28 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ba2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blocus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('date_debut', models.DateField(blank=True, null=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('periode', models.CharField(blank=True, choices=[('noel', 'Noël'), ('paques', 'Pâques'), ('mai', 'Mai'), ('juillet', 'Juillet/Août')], max_length=200)),
                ('is_current', models.BooleanField(default=False)),
                ('archived', models.BooleanField(default=False)),
                ('campus', models.ManyToManyField(to='ba2.Campus')),
            ],
        ),
    ]
