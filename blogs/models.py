import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    detail = models.TextField()
    
    author = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, 
        null=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    @property
    def get_score(self):
        return PostVote.objects.filter(post=self).aggregate(total=Sum("value"))["total"]
    
    def was_published_recently(self):
        return self.create_time >= timezone.now() - datetime.timedelta(days=1)

class Comment(models.Model):
    detail = models.TextField()
    
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE)

    def __str__(self):
        return self.detail
    
    @property
    def get_score(self):
        return PostVote.objects.filter(post=self).aggregate(total=Sum("value"))["total"]

class Tag(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)

class PostVote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)   
    author = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE)
    value = models.IntegerField(default=1)
    timestamp = models.DateTimeField(default=timezone.now)

class CommentVote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)   
    author = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE)
    value = models.IntegerField(default=1)
    timestamp = models.DateTimeField(default=timezone.now)