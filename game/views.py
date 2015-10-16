# -*- coding: utf-8 -*-
import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import JsonResponse
from qa.models import User
from models import Bigsmall
import time


caibs = lambda :random.randint(0, 1)

def game_index(request, num=None):


    if num == '1':
        reset = request.GET.get('reset')
        if reset is not None :
            try:
                user = User.objects.get(email=reset)
                bigsmall = user.game_user.get()
                bigsmall.times = 1000
                bigsmall.money = 1000
                bigsmall.save()
                return JsonResponse({'status':0,'message':'ok'})
            except:
                return JsonResponse({'status':1,'error':'503'})

        if request.GET.get('email'):
            email = request.GET.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'status':1,'error':'no user'}) #没有此用户

            try:
                m = int(request.GET.get('m'))
                if m < 1:
                    raise ValueError
            except ValueError:
                return  JsonResponse({'status':1 , 'error': 'm<1'})    # 押金小于1

            try:
                bigsmall = user.game_user.get()
            except Bigsmall.DoesNotExist:
                bigsmall = Bigsmall(user_id=user)

            if bigsmall.times < 1:
                return JsonResponse({'status':1, 'error': 'times over','money': bigsmall.money})


            bs = request.GET.get('bigsmall', '2')   # 没有押大小,就送钱

            bigsmall.times -=1
            time.sleep(5)
            if str(caibs()) == bs:
                bigsmall.money += m
                bigsmall.save()
                return JsonResponse({'status': '0', 'wl':'w', 'm': m, 'money': bigsmall.money, 'times':bigsmall.times})
            else:
                bigsmall.money -= m
                bigsmall.save()
                return JsonResponse({'status': '0', 'wl':'l', 'm': m,'money': bigsmall.money, 'times': bigsmall.times})


        g_list = {'1': 'bigsmall.html'}
        return render(request, g_list[num])
    else:
        return render(request, 'game_index.html')

def game_bs(request):
    return render(request, 'game_bs.html')

def game_honorlist(request, num=None):
    bigsmall = Bigsmall.objects.filter()[:100]
    return render(request, 'game_honor.html', {'honorlist': bigsmall})