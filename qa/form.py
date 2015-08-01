# -*- coding: utf-8 -*-
from django import forms

from models import User

class LoginForm(forms.Form):
    email = forms.CharField(max_length=254)
    password = forms.CharField(max_length=127)




error_messages = {
    'name': {
        'required': u'必须填写用户名',
        'min_length': u'用户名长度过短（3-12个字符）',
        'max_length': u'用户名长度过长（3-12个字符）',
        'invalid': u'用户名格式错误（英文字母开头，数字，下划线构成）'
    },
    'email': {
        'required': u'必须填写E-mail',
        'min_length': u'Email长度有误',
        'max_length': u'Email长度有误',
        'invalid': u'Email地址无效'
    },
    'psd': {
        'required': u'必须填写密码',
        'min_length': u'密码长度过短（6-64个字符）',
        'max_length': u'密码长度过长（6-64个字符）'
    },
}


class RegisterForm(forms.ModelForm):

    name = forms.RegexField(min_length=3,max_length=30,regex=r'^[a-zA-Z][a-zA-Z0-9_]*$',
                            error_messages=error_messages.get("name"))

    email = forms.EmailField(min_length=8, max_length=64,error_messages=error_messages.get("email"))

    psd = forms.CharField(min_length=6, max_length=64,error_messages=error_messages.get("psd"))

    introduction = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("name","email","psd")

    def clean_name(self):
        name = self.cleaned_data["name"]
        user = User.objects.filter(name=name)
        if user:
            raise forms.ValidationError(u'所填用户名已经被注册过')
        return name

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email)
        if user:
            raise forms.ValidationError(u'所填邮箱已经被注册过')
        return email