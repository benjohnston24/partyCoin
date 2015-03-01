# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.CharField(max_length=20)),
                ('party', models.CharField(max_length=200)),
                ('donor', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=3)),
                ('postcode', models.CharField(max_length=4)),
                ('donor_type', models.CharField(max_length=40)),
                ('amount', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
