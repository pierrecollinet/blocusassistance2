# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-20 13:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ba2', '0003_temoignageeleve'),
        ('blocus', '0003_professeurblocus_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('etudiant', models.CharField(max_length=100)),
                ('points_faibles', models.TextField()),
                ('points_forts', models.TextField()),
                ('amelioration', models.TextField()),
                ('professeurs', models.TextField()),
                ('qualite_assistants', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=10)),
                ('cadre_travail', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=10)),
                ('silence', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=10)),
                ('nombre_assistants', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=10)),
                ('efficacite', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=10)),
                ('avis_general', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=10)),
                ('temoignage', models.TextField(blank=True, null=True)),
                ('faculte', models.CharField(blank=True, max_length=100, null=True)),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ba2.Campus')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blocus.ModuleBlocus')),
            ],
        ),
    ]
