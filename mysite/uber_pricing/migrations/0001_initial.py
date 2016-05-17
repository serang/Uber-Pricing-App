# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('last_time_checked', models.DateTimeField(help_text='Last time surge pricing was checked')),
                ('phone_number', models.IntegerField(help_text='phone number to contact buyer')),
                ('last_surge_multiplier', models.FloatField(help_text='last surge multiplier recorded')),
                ('surge_threshold', models.FloatField(help_text='surge pricing threshold set by user. Contact if below')),
                ('contacted', models.BooleanField(help_text='have been contacted or not', default=False)),
                ('current_address', models.CharField(help_text='users current address', max_length=1000)),
            ],
        ),
    ]
