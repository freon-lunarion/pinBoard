from .models import *
from datetime import datetime 
from django import forms
from django.contrib.admin import widgets
from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from shared.models import *
from tinymce.widgets import TinyMCE

class QuizBankForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    detail = forms.CharField(required=False, widget=forms.Textarea)
    tryout_minScore = forms.IntegerField(min_value=0,initial=0)
    tryout_displayNum = forms.IntegerField(min_value=1,initial=5)
    class Meta:
        model = QuizBank
        fields = ['title', 'detail', 'tryout_minScore', 'tryout_displayNum']

# REF: https://www.caktusgroup.com/blog/2018/05/07/creating-dynamic-forms-django/
class QuestionForm(forms.ModelForm):
    detail = forms.CharField(required=True, widget=forms.Textarea)
    options_0 = forms.CharField(required =True,label="Option 1")
    true_0 = forms.BooleanField(label="is the right answer?")

    options_1 = forms.CharField(required =True,label="Option 2")
    true_1 = forms.BooleanField(label="is the right answer?", initial=1)

    options_2 = forms.CharField(required =True,label="Option 3")
    true_2 = forms.BooleanField(label="is the right answer?", initial=2)

    options_3 = forms.CharField(required =True,label="Option 4")
    true_3 = forms.BooleanField(label="is the right answer?",initial=3)


    class Meta:
        model = Question
        fields = ['detail']
    
    def save(self):
        question = self.instance
        question.detail = self.cleaned_data["detail"]

        question.options_set.all().delete()
        for i in range(4):
            option = self.cleaned_data["options_{}".format(i)]
            isTrue = self.cleaned_data["true_{}".format(i)]
            Options.objects.create(question = Question, detail = option, isCorrect = isTrue)
    
