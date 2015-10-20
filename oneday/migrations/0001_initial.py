# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0005_user_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daytry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=127)),
                ('image', models.URLField(null=True, blank=True)),
                ('d_type', models.CharField(max_length=63)),
                ('introduction', models.CharField(max_length=255)),
                ('day_time', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('user', models.ForeignKey(to='qa.User')),
            ],
        ),
    ]
