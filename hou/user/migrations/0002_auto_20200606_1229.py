# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-06-06 04:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='qq',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='QQ'),
        ),
    ]
