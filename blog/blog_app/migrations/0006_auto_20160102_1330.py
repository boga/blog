# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-02 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0005_auto_20160102_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='notes',
            field=models.ManyToManyField(related_name='tags', to='blog_app.Note'),
        ),
    ]
