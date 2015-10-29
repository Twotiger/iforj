# -*- coding: utf-8 -*-
"""iforjcom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
# from qa import views
from game import views as game_view
from oneday import views as day_view

######GAME##########
game_patterns = [
    url(r'^$', game_view.game_index),   # 主页
    url(r'^(\d+)/$', game_view.game_index, name='game'), # 管理游戏列表
    url(r'^(\d+)/honorlist/$', game_view.game_honorlist),   # 荣誉榜单
    # url(r'^(\d+)$', game_view.game),
]

#######ONEDAY#######
day_patterns = [
    url(r'^$', day_view.index), #首页
    url(r'^addreleaseday/$', day_view.addreleaseday, name='addreleaseday'), # 发布每日一练
    url(r'^(\d+)/$', day_view.showoneday, name='showoneday'), # 展示每日一练
    url(r'^addreply/$', day_view.addreply, name='addreply'), # 评论
    url(r'^agreereply/$', day_view.agreereply, name='agreereply'), # 赞同评论

    # url(r'^')
]


urlpatterns = [
    url(r'^$', 'qa.views.index', name='index'),
    url(r'^qntoken/$','qa.views.qntoken'),
    url(r'^top/$', 'qa.views.top'),
    url(r'^login/$', 'qa.views.login'),
    url(r'^logout/$', 'qa.views.logout'),
    url(r'^register/$', 'qa.views.register', name='register'),                  # 注册
    url(r'^question/(\d+)$', 'qa.views.getquestion', name='question'),          # 问题
    url(r'^search/$', 'qa.views.search'),
    url(r'^programmer/(\d+)$', 'qa.views.programmer', name='programmer'),

    url(r'^agreeanswer/$','qa.views.agree_answer'), # ajax提交 赞同的回答
    url(r'^validate/(\w+)$', 'qa.views.validate'),   # 验证用户

    url(r'^askquestion/$', 'qa.views.askquestion'),



    url(r'^commit/post/addanswer$', 'qa.views.commit_post_add'),    # 提交答案
    url(r'^commit/post/updateanswer$','qa.views.commit_post_update'),   #

    url(r'^commit/post/getcomment$', 'qa.views.getcomment'),  # 废除
    url(r'^commit/post/addcomment$', 'qa.views.addcomment'),   # 提交答案

    #url(r'^test/$','qa.views.test'),    # test markdown
    url(r'^about/', 'qa.views.about_us'),   # 关于我们

    url(r'^admin/', include(admin.site.urls)),


    url(r'^about/', 'qa.views.about_us'),

    url(r'^uploadImage$', 'qa.views.uploadImage', name="uploadImage"),
    url(r'^follow/(\d+)$', 'qa.views.follow', name='follow'),
    url(r'^unfollow/(\d+)$', 'qa.views.unfollow', name='unfollow'),
    url(r'^edit-profile/$', 'qa.views.editProfile', name="edit-profile"),

    url(r'^verificationcode/$', 'qa.views.verificationcode', name="verificationcode"),

    ######GAME##########
    url(r'game/', include(game_patterns, namespace='game')),
    ####################
    ######ONEDAY########
    url(r'day/', include(day_patterns, namespace='day')),
    ####################
]
