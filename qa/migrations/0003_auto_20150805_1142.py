# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0002_auto_20150805_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='agree_num',
            field=models.IntegerField(default=0),
        ),
    ]
