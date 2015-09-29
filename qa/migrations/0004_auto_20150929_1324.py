# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0003_auto_20150909_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='follower', to='qa.User'),
        ),
        migrations.AlterField(
            model_name='questiontype',
            name='name',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
