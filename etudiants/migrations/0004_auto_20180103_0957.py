# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-03 09:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('etudiants', '0003_etudiant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etudiant',
            name='etude',
        ),
        migrations.RemoveField(
            model_name='etudiant',
            name='faculte',
        ),
        migrations.RemoveField(
            model_name='etudiant',
            name='universite',
        ),
        migrations.RemoveField(
            model_name='etudiant',
            name='user',
        ),
        migrations.DeleteModel(
            name='Etudiant',
        ),
    ]
