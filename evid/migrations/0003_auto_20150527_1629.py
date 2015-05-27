# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evid', '0002_auto_20150527_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kantor',
            name='pohlavi',
            field=models.CharField(max_length=10, choices=[(b'M', b'Mu?'), (b'Z', b'Zena.')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='pohlavi',
            field=models.CharField(max_length=10, choices=[(b'M', b'Mu?'), (b'Z', b'Zena.')]),
        ),
    ]
