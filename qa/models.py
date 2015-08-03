# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
import hashlib

# Create your models here.

class User(models.Model):
    """用户表"""
    name = models.CharField(max_length=80, unique=True)  # 名字
    psd = models.CharField(max_length=127)   # 密码
    email = models.CharField(max_length=254, unique=True)
    register_time = models.DateTimeField(auto_now=True) # 注册时间
    last_time = models.DateTimeField(auto_now=True)     # 最后次登陆时间
    is_veri = models.BooleanField(default=False)    # 是否验证过
    vericode = models.CharField(max_length=40,  null=True, blank=True)  # 验证码

    # url = models.CharField(max_length=127) # 存储成好看的拼音
    introduction = models.CharField(max_length=127,null=True, blank=True) # 简介
    image = models.URLField(null=True, blank=True)   # 头像
    login_error = models.PositiveSmallIntegerField(default=0)   # 当错误登陆+1
    agree_num = models.PositiveIntegerField(default=0)  # 赞同数
    viewed = models.PositiveIntegerField(default=0)   # 被浏览次数



    def save(self, *args, **kwargs):
        self.psd = hashlib.sha1(self.psd).hexdigest()
        self.vericode = hashlib.sha1(self.email+'4646868').hexdigest()
        super(User,self).save(*args,**kwargs)



    def __unicode__(self):
        return self.name


class QuestionType(models.Model):
    """问题类型 比如 django/爬虫"""
    name = models.CharField(max_length=15)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    """问题表"""
    user = models.ForeignKey(User)
    title = models.CharField(max_length=127)
    text = models.TextField()
    q_datetime = models.DateTimeField(auto_now=True) # 回复时间
    q_times = models.PositiveSmallIntegerField(default=0)   # 回复数量
    q_type = models.ForeignKey(QuestionType, null=True, blank=True)

    class Meta:
        ordering = ('q_datetime',)

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    """答案表"""
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)  # 用户外键
    text = models.TextField()   # 答案
    agree_user = models.ForeignKey(User ,related_name='Answer_agree_user', null=True, blank=True) # 赞同的人
    a_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s"%self.text




admin.site.register((User, Question , Answer, QuestionType))