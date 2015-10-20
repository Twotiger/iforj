# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oneday', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='daytry',
            name='is_veri',
            field=models.BooleanField(default=False),
        ),
    ]
