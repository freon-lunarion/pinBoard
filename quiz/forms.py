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

class Question2Form(forms.ModelForm):
    # detail = forms.CharField(required=True, widget=forms.Textarea)
    quizBank = forms.ModelChoiceField(queryset= QuizBank.objects.all(),widget=forms.HiddenInput())
    
    class Meta:
        model = Question
        fields = ('detail','quizBank')

class OptionsForm(forms.ModelForm):
    question = forms.ModelChoiceField(queryset= Question.objects.all(),widget=forms.HiddenInput())

    isCorrect = forms.BooleanField(required =False, label="is the right answer?")
    detail = forms.CharField(required =True,label="Option")
    
    class Meta:
        model = Options
        fields = ('question', 'detail', 'isCorrect')

# OptionsFormSet = forms.inlineformset_factory(Question, Options, form=OptionsForm, extra=1)

# REF: https://www.caktusgroup.com/blog/2018/05/07/creating-dynamic-forms-django/
class QuestionForm(forms.ModelForm):
    quizBank = forms.ModelChoiceField(queryset=QuizBank.objects.all(),widget=forms.HiddenInput())
    
    # detail = forms.CharField(required=True, widget=forms.Textarea)
    options_0 = forms.CharField(required =True,label="Option 1")
    true_0 = forms.BooleanField(required =False, label="is the right answer?")

    options_1 = forms.CharField(required =True,label="Option 2")
    true_1 = forms.BooleanField(required =False,label="is the right answer?",)

    options_2 = forms.CharField(required =True,label="Option 3")
    true_2 = forms.BooleanField(required =False,label="is the right answer?",)

    options_3 = forms.CharField(required =True,label="Option 4")
    true_3 = forms.BooleanField(required =False,label="is the right answer?",)


    class Meta:
        model = Question
        fields = ['detail','quizBank']

