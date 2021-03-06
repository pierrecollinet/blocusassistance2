# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-29 10:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ba2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etude',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abreviation', models.CharField(blank=True, max_length=200, null=True)),
                ('nom', models.CharField(max_length=200)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='mes_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Faculte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abreviation', models.CharField(blank=True, max_length=200, null=True)),
                ('nom', models.CharField(max_length=200)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='mes_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Universite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('abreviation', models.CharField(blank=True, max_length=200, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='mes_images/')),
            ],
        ),
        migrations.AddField(
            model_name='faculte',
            name='universite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ba2.Universite'),
        ),
        migrations.AddField(
            model_name='etude',
            name='faculte',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ba2.Faculte'),
        ),
    ]
