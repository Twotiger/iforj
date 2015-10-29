# -*- coding: utf-8 -*-
#__author__ = 'twotiger'
from django import template
from datetime import datetime
from django.utils.timezone import utc
from math import sqrt

register = template.Library()

@register.filter(name='isince')
def isince(value):
    """返回距离现在多久了"""
    now = datetime.utcnow().replace(tzinfo=utc)
    subtime = now - value
    if subtime.days > 29:
        return value.strftime("%Y-%m-%d")
    elif subtime.days > 0:
        return "%s天之前" % subtime.days
    elif subtime.seconds > 3599 :
        return "%s个小时之前"% (subtime.seconds/3600)
    elif subtime.seconds > 59:
        return "%s分种之前" % (subtime.seconds/60)
    else:
        return "刚刚"

@register.filter(name='changecolor')
def getcolor(num):
    # 0-255颜色  0-300 num
    c = 255-sqrt(99*num)
    if c < 0:
        return "ffffff"
    x = "%x"%int(c)
    if len(x) == 1:
        return ("0"+x)*3
    return x*3