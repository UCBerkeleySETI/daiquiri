# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-21 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_jobs', '0008_job_error_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(choices=[('QUERY', 'Query'), ('CUTOUT', 'Cutout')], max_length=10),
        ),
    ]
