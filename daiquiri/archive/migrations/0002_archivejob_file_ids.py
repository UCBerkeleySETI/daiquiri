# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-11 16:01
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_archive', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivejob',
            name='file_ids',
            field=jsonfield.fields.JSONField(default='', help_text='IDs of files the files to download.', verbose_name='Files'),
            preserve_default=False,
        ),
    ]
