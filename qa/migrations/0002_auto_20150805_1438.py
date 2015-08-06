# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='agree_num',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='q_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
