# -*- coding: utf-8 -*-
import re
from django import forms

from models import User


class LoginForm(forms.Form):
    """简单的登陆"""
    email = forms.CharField(max_length=254)
    password = forms.CharField(max_length=127)


error_messages = {
    'name': {
        'required': u'必须填写用户名',
        'min_length': u'用户名长度过短（3-12个字符）',
        'max_length': u'用户名长度过长（3-12个字符）',
        'invalid': u'用户名格式错误（只能包含汉字,英文字母，数字，下划线）'
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
    # name = forms.RegexField(min_length=3, max_length=30, regex=r'^[a-zA-Z][a-zA-Z0-9_]*$',
    #                         error_messages=error_messages.get("name"))
    name = forms.RegexField(min_length=2, max_length=30, regex='^\w+$',
                            error_messages=error_messages.get("name"))
    email = forms.EmailField(min_length=8, max_length=84, error_messages=error_messages.get("email"))
    psd = forms.CharField(min_length=6, max_length=64, error_messages=error_messages.get("psd"))
    introduction = forms.CharField(required=False)

    denyName = [u'管理员', u'admin', u'root', u'匿名', u'版主', u'站长', u'屌', u'逼', u'fuck']

    class Meta:
        model = User
        fields = ("name","email","psd")

    def clean_name(self):
        name = self.cleaned_data["name"]
        user = User.objects.filter(name=name)
        if user:
            raise forms.ValidationError(u'所填用户名已经被注册过')
        for deny in self.denyName:
            if deny in name:
                raise forms.ValidationError(u'禁止的用户名')

        return name

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email)
        if user:
            raise forms.ValidationError(u'所填邮箱已经被注册过')
        return email


# CHOICES = []
# questiontype = QuestionType.objects.all()
# for qtype in questiontype:
#     CHOICES.append([qtype.id, qtype.name])
# QTYPE_CHOICES = tuple(CHOICES)

class QuestionForm(forms.Form):
    title = forms.CharField(min_length=5, max_length=127)
    text = forms.CharField(max_length=1023)
    q_type = forms.CharField(min_length=2, max_length=15)

#    def clean_text(self):
#        html = self.cleaned_data['text']
#
#        text = re.sub('<\s*script\s*>', '&ltscript&gt;',html)
#
#        return text


class AnswerForm(forms.Form):
    qid = forms.IntegerField()
    text = forms.CharField(max_length=1023)


class UpAnswerForm(forms.Form):
    get_id = forms.IntegerField()
    text = forms.CharField(max_length=1023)

#    def clean_text(self):
#        html = self.cleaned_data['text']
#        text = re.sub('<\s*script\s*>', '&lt;script&gt;',html)
#        # text = html.replace('<script>', '&ltscript>;').replace('>', '&gt;')
#        return text


class UploadImageForm(forms.Form):
    user_id = forms.CharField()
    user_image = forms.ImageField()

class EditProfileForm(forms.Form):
    new_introduction = forms.CharField(required=False, max_length=127)

# class EditProfileForm(forms.Form):
    # new_email = forms.EmailField(min_length=8, max_length=84, error_messages=error_messages.get("email"))
    # new_introduction = forms.CharField(required=False)

    # class Meta:
    #     model = User
    #     fields = ("new_email",)

    # def clean_new_email(self):
    #     user = User.objects.filter(email=new_email)
    #     if user:
    #         raise forms.ValidationError(u'所填邮箱已经被注册过')
    #     return new_email


