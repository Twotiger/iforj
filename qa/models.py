# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

# Create your models here.


class User(models.Model):
    """用户表"""
    name = models.CharField(max_length=80, unique=True)  # 名字
    psd = models.CharField(max_length=127)   # 密码
    email = models.CharField(max_length=254, unique=True)
    register_time = models.DateTimeField(auto_now_add=True) # 注册时间
    last_time = models.DateTimeField(auto_now=True)     # 最后次登陆时间
    is_veri = models.BooleanField(default=False)    # 是否验证过
    vericode = models.CharField(max_length=40,  null=True, blank=True)  # 验证码编码,发送到邮箱验证
    real_ip = models.GenericIPAddressField(null=True, blank=True)  # 注册时的ip地址
    # url = models.CharField(max_length=127) # 存储成好看的拼音
    introduction = models.CharField(max_length=127, null=True, blank=True) # 简介
    image = models.URLField(null=True, blank=True)   # 头像
    login_error = models.PositiveSmallIntegerField(default=0)   # 当错误登陆+1
    agree_num = models.IntegerField(default=0)  # 赞同数(当问答问题的时候被赞+1)
    viewed = models.PositiveIntegerField(default=0)   # 被浏览次数
    # 关注,自引用关系
    following = models.ManyToManyField("self", symmetrical=False, related_name="follower")

    def __unicode__(self):
        return self.name


class QuestionType(models.Model):
    """问题类型 比如 django/爬虫"""
    name = models.CharField(max_length=15, null=True)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    """问题表"""
    user = models.ForeignKey(User)
    title = models.CharField(max_length=127)
    text = models.TextField()
    q_datetime = models.DateTimeField(auto_now_add=True) # 创建时间
    q_times = models.PositiveSmallIntegerField(default=0)   # 回复数量
    # 新增赞同数量
    q_type = models.ForeignKey(QuestionType, null=True, blank=True) # 问题类型

    class Meta:
        ordering = ('-q_datetime',)

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    """答案表"""
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)  # 回答者
    text = models.TextField()   # 答案
    agree_user = models.ManyToManyField(User, related_name='answer_user')  # 赞同的人
    agree_num = models.SmallIntegerField(default=0)  # 赞同人的数量
    a_time = models.DateTimeField(auto_now_add=True)    # 创建时间
    weight = models.PositiveSmallIntegerField(null=True)    # 权重.
    waring = models.PositiveSmallIntegerField(null=True)    # 有人举报+1

    def __unicode__(self):
        return "%s" % self.text


class Comment(models.Model):
    """评论"""
    user = models.ForeignKey(User)
    text = models.TextField()
    c_time = models.DateTimeField(auto_now_add=True) # 创建时间
    answer = models.ForeignKey(Answer)

    def __unicode__(self):
        return self.text


admin.site.register((User, Question , Answer, QuestionType))
