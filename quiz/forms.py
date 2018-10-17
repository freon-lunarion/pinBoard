from django import forms
from django.contrib.admin import widgets
from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from shared.models import *
from tinymce.widgets import TinyMCE
from datetime import datetime 

class AddRoomForm(forms.Form):
    title = forms.CharField(max_length=128)
    detail = forms.CharField(required=False, widget=forms.Textarea)

    submit_beginTime = forms.DateTimeField(initial=datetime.now())
    submit_endTime = forms.DateTimeField(initial=datetime.now())

    tryout_minScore = forms.IntegerField(initial=0) 
    tryout_displayNum = forms.IntegerField(initial=5,min_value=0)

    tryout_beginTime = forms.DateTimeField(initial=datetime.now())
    tryout_endTime = forms.DateTimeField(initial=datetime.now())

