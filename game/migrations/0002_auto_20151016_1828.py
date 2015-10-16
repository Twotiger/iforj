# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bigsmall',
            options={'ordering': ('-money',)},
        ),
        migrations.AlterField(
            model_name='bigsmall',
            name='user_id',
            field=models.ForeignKey(related_name='game_user', to='qa.User'),
        ),
    ]
