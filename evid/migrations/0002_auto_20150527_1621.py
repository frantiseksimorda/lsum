# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evid', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kantor',
            name='cip',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='kantor',
            name='email',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='kantor',
            name='login',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='cip',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='login',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
