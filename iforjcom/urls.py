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

urlpatterns = [
    url(r'^$', 'qa.views.index', name='index'),
    url(r'^login/$', 'qa.views.login'),
    url(r'^logout/$', 'qa.views.logout'),
    url(r'^register/$', 'qa.views.register', name='register'),
    url(r'^question/(\d)+$', 'qa.views.getquestion', name='question'),
    url(r'^search/$', 'qa.views.search'),

    url(r'^askquestion/$', 'qa.views.askquestion'),
    url(r'^testtwo/$', 'qa.views.testtwo'), # will be del
    url(r'^commit/post/getcomment$', 'qa.views.getcomment'),

    url(r'^commit/post/addanswer$', 'qa.views.commit_post_add'),
    url(r'^admin/', include(admin.site.urls)),
]
#/commit/post/getcomment'