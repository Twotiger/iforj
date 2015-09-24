# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0002_user_real_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='real_ip',
            field=models.GenericIPAddressField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='register_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
