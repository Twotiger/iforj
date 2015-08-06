# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0003_auto_20150805_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='a_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='agree_num',
            field=models.SmallIntegerField(default=0),
        ),
    ]
