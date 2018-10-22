from shared.models import *
from livesession.models import LiveQuestionSession

# Create your models here.

# Post, with kinds of article post, image post and youtube post
class Post(Content):
    title = models.CharField(max_length=150)
    kind = models.CharField(max_length=20, default='Post')
    is_pinned = models.BooleanField(default=False)
    pin_board = models.ForeignKey(PinBoard, on_delete=models.CASCADE, default=None, blank=True, null=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def pinned(self, moderator, is_pinned=True):
        if moderator.is_superuser:
            self.is_pinned = is_pinned
            self.operator = moderator
            self.save()

    def is_favorite_of(self, user):
        is_favorite = UserFavorite.objects.filter(user=user, post=self)
        return True if is_favorite else False

    def __str__(self):
        """String for representing the Post object."""
        return f'{self.title}'

    # Text description about number of comments for the post
    @property
    def comment_count_string(self):
        count = Comment.objects.filter(parent=self).count()
        count_string = ''
        if count == 0:
            count_string = "No Comments"
        if count == 1:
            count_string = "1 Comment"
        if count > 1:
            count_string = str(count) + ' Comments'
        return count_string

# Post comment
class Comment(Content):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.detail}'

    def publish(self):
        self.published_date = timezone.now()
        self.save()

# Qna Question
class QnaQuestion(Content):
    title = models.CharField(max_length=150)
    kind = models.CharField(max_length=20, default='Question')
    is_pinned = models.BooleanField(default=False)
    pin_board = models.ForeignKey(PinBoard, on_delete=models.CASCADE, default=None, blank=True, null=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    is_live_question = models.BooleanField(default=False)
    parent = models.ForeignKey(LiveQuestionSession, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # Answers for the question
    @property
    def answers(self):
        return sorted(QnaAnswer.objects.filter(parent=self),
                        key=lambda x: (1 if x.is_correct else 0, x.score, -x.published_date.toordinal() if x.published_date
                        else 0), reverse=True)

    # Boolean value about whether a question is solved
    @property
    def solved(self):
        return QnaAnswer.objects.filter(parent=self, is_correct=True).count() > 0

    # Text description about whether a question is solved
    @property
    def question_status(self):
        return 'Solved' if self.solved else 'Unsolved'

    # Text description about number of answers for the question
    @property
    def response_count_string(self):
        count = len(self.answers)
        count_string = ''
        if count == 0:
            count_string = "No Responses"
        if count == 1:
            count_string = "1 Response"
        if count > 1:
            count_string = str(count) + ' Responses'
        return count_string


# Answer for Qna Question
class QnaAnswer(Content):
    is_correct = models.BooleanField(default=False)
    parent = models.ForeignKey(QnaQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.detail}'

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def set_correct(self):
        Vote.vote(self.id, self.parent.author.id, 5)
        self.is_correct = True
        self.save()
