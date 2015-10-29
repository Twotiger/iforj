# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bigsmall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('times', models.PositiveSmallIntegerField(default=1000)),
                ('money', models.IntegerField(default=1000)),
                ('user_id', models.ForeignKey(related_name='game_user', to='qa.User')),
            ],
            options={
                'ordering': ('-money',),
            },
        ),
    ]
