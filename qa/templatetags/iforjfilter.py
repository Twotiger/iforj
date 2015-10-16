# -*- coding: utf-8 -*-
#__author__ = 'twotiger'
from django import template
from datetime import datetime
from django.utils.timezone import utc

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
        return "%s小时之前"% (subtime.seconds/3600)
    elif subtime.seconds > 59:
        return "%s分种之前" % (subtime.seconds/60)
    else:
        return "刚刚"
