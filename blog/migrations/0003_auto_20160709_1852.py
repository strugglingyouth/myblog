# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-09 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='website',
            field=models.URLField(null=True, verbose_name=b'\xe7\xab\x99\xe7\x82\xb9\xe4\xbf\xa1\xe6\x81\xaf'),
        ),
    ]