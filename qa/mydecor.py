# -*- coding: utf-8 -*-
__author__ = 'twotiger'
from django.shortcuts import render
from models import User


def islogin(func):
    def is_login(request):
        getname = request.session.get('name').split('$')[0]
        try:
            user = User.objects.get(name=getname)
        except User.DoesNotExist:
            return rendeer(request, 'register.html')
        func()
    return is_login

