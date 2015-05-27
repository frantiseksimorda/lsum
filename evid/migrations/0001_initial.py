# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kantor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jmeno', models.CharField(max_length=50)),
                ('prijmeni', models.CharField(max_length=50)),
                ('login', models.CharField(max_length=20)),
                ('pohlavi', models.CharField(max_length=10)),
                ('kod_baka', models.CharField(max_length=20)),
                ('datum_pridani', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('cip', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('aktivni', models.BooleanField()),
            ],
            options={
                'verbose_name': 'kantor',
                'verbose_name_plural': 'kantori',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jmeno', models.CharField(max_length=50)),
                ('prijmeni', models.CharField(max_length=50)),
                ('login', models.CharField(max_length=20)),
                ('pohlavi', models.CharField(max_length=10)),
                ('kod_baka', models.CharField(max_length=20)),
                ('datum_pridani', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('cip', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('aktivni', models.BooleanField()),
            ],
            options={
                'verbose_name': 'student',
                'verbose_name_plural': 'studenti',
            },
        ),
        migrations.CreateModel(
            name='Trida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zkratka', models.CharField(max_length=5)),
                ('rok', models.DateField(verbose_name=b'')),
                ('pismenko', models.CharField(max_length=2)),
                ('delka_studia', models.IntegerField()),
                ('rok_zalozeni', models.DateField()),
            ],
            options={
                'verbose_name': 'trida',
                'verbose_name_plural': 'tridy',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='trida',
            field=models.ForeignKey(to='evid.Trida'),
        ),
    ]
