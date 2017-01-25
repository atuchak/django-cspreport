# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 13:22
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CSPReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.TextField(blank=True, default='', null=True)),
                ('document_uri', models.TextField()),
                ('blocked_uri', models.TextField()),
                ('referrer', models.TextField(blank=True, default='', null=True)),
                ('body', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
                ('request_meta', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
