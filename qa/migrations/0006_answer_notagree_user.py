# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0005_answer_waring'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='notagree_user',
            field=models.ManyToManyField(related_name='notanswer_user', to='qa.User'),
        ),
    ]
