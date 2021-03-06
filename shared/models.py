from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.utils import timezone
from tinymce import models as tinymce_models
import datetime

# Create your models here.

class UserProfile(models.Model):
    # REF : https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    # REF : https://stackoverflow.com/questions/6396442/add-image-avatar-field-to-users-in-django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.TextField()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    # Score that a user receives as their work being voted by others
    @property
    def score(self):
        return sum([c.score for c in Content.objects.filter(author=self.user)])

    # Ids of user's favorite posts
    @property
    def favorites_id(self):
        return [x.content.id for x in sorted(UserFavorite.objects.filter(user=self.user), key=lambda x: -x.create_time.timestamp())]

    # User's favorite posts
    @property
    def favorites(self):
        from blogs.models import Post, QnaQuestion
        contents = [rec.content for rec in sorted(UserFavorite.objects.filter(user=self.user),
                                                  key=lambda x: -x.create_time.timestamp())]
        res = []
        for content in contents:
            post_que = Post.objects.filter(id=content.id)
            if post_que.count() == 1:
                res.append(Post.objects.get(id=content.id))
            else:
                question_que = QnaQuestion.objects.filter(id=content.id)
                if question_que.count() == 1:
                    res.append(QnaQuestion.objects.get(id=content.id))
        return res

    # How many qna answers did the user give
    @property
    def total_answer_num(self):
        from blogs.models import QnaAnswer
        return QnaAnswer.objects.filter(author=self.user).count()

    # How many qna answers that the user gave were approved as correct answer for qna questions
    @property
    def correct_answer_num(self):
        from blogs.models import QnaAnswer
        return QnaAnswer.objects.filter(author=self.user, is_correct=True).count()

    # The ratio of #correct answer / #total answer
    @property
    def correct_answer_percentage(self):
        return f'{round(100 * (self.correct_answer_num / self.total_answer_num) if self.total_answer_num else 0, 1)}%'

    # Five posts with highest score
    @property
    def top_five_posts(self):
        from blogs.models import Post, QnaQuestion
        contents = sorted([rec for rec in Content.objects.filter(author=self.user)],
                          key=lambda x: (x.score, x.create_time.timestamp()), reverse=True)
        res = []
        for content in contents:
            post_que = Post.objects.filter(id=content.id)
            if post_que.count() == 1:
                res.append(Post.objects.get(id=content.id))
            else:
                question_que = QnaQuestion.objects.filter(id=content.id)
                if question_que.count() == 1:
                    res.append(QnaQuestion.objects.get(id=content.id))
            if len(res) == 5:
                break
        return res

    # Score rank
    @property
    def rank(self):
        return len(list(filter(lambda x: x.score > self.score, UserProfile.objects.all()))) + 1

# Pinboard model which is not used in the demo. For further development.
class PinBoard(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @staticmethod
    def create(title, creator, detail=''):
        return PinBoard.objects.create(title=title, detail=detail, creator=creator)

# Base model for post, comment, qna question, qna answer and quiz quesiton, supporting voting, tagging and saving as favorite
class Content(models.Model):
    detail = tinymce_models.HTMLField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    @property
    def score(self):
        score = Vote.objects.filter(content=self).aggregate(total=Sum("value"))["total"]
        return score if score else 0
    
    @property
    def num_voter(self):
        num_voter = Vote.objects.filter(content=self).aggregate(total=Count("value"))["total"]
        return num_voter if num_voter else 0

    @property
    def is_published_recently(self):
        return self.create_time >= timezone.now() - datetime.timedelta(days=1)

    @property
    def tags(self):
        return [obj.tag.title for obj in ContentTag.objects.filter(content__exact=self)]


# Tags
class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    @staticmethod
    def create(title):
        return Tag.objects.create(title=title)


# Relate contents to tags
class ContentTag(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)

    class Meta:
        unique_together = ("content", "tag")

    @staticmethod
    def create(content_id, tag_id):
        content = get_object_or_404(Content, id=content_id)
        tag = get_object_or_404(Tag, id=tag_id)
        return ContentTag.objects.create(content=content, tag=tag)

# Store voting data
class Vote(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)

    @staticmethod
    def vote(content_id, user_id, value):
        content = get_object_or_404(Content, id=content_id)
        user = get_object_or_404(User, id=user_id)
        Vote.objects.create(content=content, user=user, value=value)
        return content.score

    @staticmethod
    def exist(content_id, user_id):
        content = get_object_or_404(Content, id=content_id)
        user = get_object_or_404(User, id=user_id)
        if Vote.objects.filter(content=content, user=user).exists():
            return 1
        else:
            return 0

# Relate users to favorite posts
class UserFavorite(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("content", "user")

    @staticmethod
    def create(content_id, user_id):
        content = get_object_or_404(Content, id=content_id)
        user = get_object_or_404(User, id=user_id)
        return UserFavorite.objects.create(content=content, user=user)