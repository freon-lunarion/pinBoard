import datetime
from django.db import models
from shared.models import *

# Each Quiz is a question bank, which can be use for one theme,a course or a topic.
class QuizBank(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField(blank=True, null=True) # this for decription of the quiz or instruction

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # creator will have special previllge to edit the setting of this quiz

    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)

    # range time quiz (bank) accept the new question. Before and after that time, the antoher user cannot submit new questions
    submit_beginTime = models.DateTimeField(default=timezone.now)
    submit_endTime = models.DateTimeField(default=timezone.now)

    # setting for displaying question
    tryout_minScore = models.IntegerField(default=0) # only questions with score above this limit will be use in tryou session 
    tryout_displayNum = models.IntegerField(default=5) # how many question displayed on tryout

    # range time quiz (bank) can be use for tryout 
    tryout_beginTime = models.DateTimeField(default=timezone.now)
    tryout_endTime = models.DateTimeField(default=timezone.now)


    def is_submit_time(self):
        if (submit_beginTime <= timezone.now and timezone.now <= submit_endTime):
            return True
        else:
            return False
        
    
    def is_tryout_time(self):
        if (tryout_beginTime <= timezone.now and timezone.now <= tryout_endTime):
            return True
        else:
            return False


    def __str__(self):
        """String for representing the QuizBank object."""
        return f'{self.title}, created by {self.creator}'
        

class Question(Content):
    quizBank = models.ForeignKey(QuizBank, on_delete=models.CASCADE)
    
class Options(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    detail = models.TextField()
    isCorrect = models.BooleanField(default=False)