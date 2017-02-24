# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 02:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg', '0002_book_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='review',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='books',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='users',
        ),
        migrations.AddField(
            model_name='rating',
            name='review',
            field=models.CharField(max_length=255, null=True),
        ),
    ]