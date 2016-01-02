# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-02 09:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_auto_20160102_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
        ),
    ]
