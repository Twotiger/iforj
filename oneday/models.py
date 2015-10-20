# -*- coding: utf-8 -*-
from django.db import models
from qa.models import User

class Daytry(models.Model):
    title = models.CharField(max_length=127)    # 标题
    image = models.URLField(null=True, blank=True)   # 预览图
    d_type = models.CharField(max_length=63)    # 题目类型
    introduction = models.CharField(max_length=255) # 简介
    day_time = models.DateTimeField(auto_now=True)   # 发表日期
    user = models.ForeignKey(User)  # 作者
    text = models.TextField()   # 文本
    is_veri = models.BooleanField(default=False) #是否验证过

    def __unicode__(self):
        return "%s"%self.day_time