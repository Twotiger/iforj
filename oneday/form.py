# -*- coding: utf-8 -*-
__author__ = 'twotiger'
from django import forms
from models import Daytry
# from qa.models import QuestionType

class Daytryform(forms.ModelForm):
    d_type = forms.CharField(min_length=2, max_length=15)

    class Meta:
        model = Daytry
        fields = ['title', 'image','introduction', 'text']

    def clean_text(self):
        text = self.cleaned_data["text"]
        if text.startswith('<div id="epiceditor-preview">'):
            return text
        else:
            raise forms.ValidationError(u'非法字符串')


