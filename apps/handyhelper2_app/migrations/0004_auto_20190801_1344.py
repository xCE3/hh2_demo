# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-01 18:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handyhelper2_app', '0003_auto_20190801_1340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='descriptionription',
            new_name='description',
        ),
    ]
