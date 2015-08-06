# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('a_time', models.DateTimeField(auto_now=True)),
                ('weight', models.PositiveSmallIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('answer', models.ManyToManyField(related_name='comment_answer', to='qa.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=127)),
                ('text', models.TextField()),
                ('q_datetime', models.DateTimeField(auto_now=True)),
                ('q_times', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ('q_datetime',),
            },
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
                ('psd', models.CharField(max_length=127)),
                ('email', models.CharField(unique=True, max_length=254)),
                ('register_time', models.DateTimeField(auto_now=True)),
                ('last_time', models.DateTimeField(auto_now=True)),
                ('is_veri', models.BooleanField(default=False)),
                ('vericode', models.CharField(max_length=40, null=True, blank=True)),
                ('introduction', models.CharField(max_length=127, null=True, blank=True)),
                ('image', models.URLField(null=True, blank=True)),
                ('login_error', models.PositiveSmallIntegerField(default=0)),
                ('agree_num', models.PositiveIntegerField(default=0)),
                ('viewed', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='q_type',
            field=models.ForeignKey(blank=True, to='qa.QuestionType', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(to='qa.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to='qa.User'),
        ),
        migrations.AddField(
            model_name='answer',
            name='agree_user',
            field=models.ManyToManyField(related_name='answer_user', to='qa.User'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='qa.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(to='qa.User'),
        ),
    ]
