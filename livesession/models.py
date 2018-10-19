from django.db import models
from shared.models import *

# Create your models here.
class LiveQuestionSession(Content):
    title = models.CharField(max_length=150)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

