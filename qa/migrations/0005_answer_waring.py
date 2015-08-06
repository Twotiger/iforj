# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0004_auto_20150805_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='waring',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
