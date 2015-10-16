# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='real_ip',
            field=models.IPAddressField(null=True, blank=True),
        ),
    ]
