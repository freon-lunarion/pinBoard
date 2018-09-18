import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    detail = models.TextField()
    score = models.IntegerField()
    # creator = models.ForeignKey(User)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    is_pinned = models.BooleanField()

    def __str__(self):
        return self.title
    
    def was_published_recently(self):
        return self.create_time >= timezone.now() - datetime.timedelta(days=1)

class Comment(models.Model):
    detail = models.TextField()
    score = models.IntegerField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    # creator = models.ForeignKey(User)
    def __str__(self):
        return self.detail

class Tag(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)