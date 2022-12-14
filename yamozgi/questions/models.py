from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "категория вопроса"
        verbose_name_plural = "категории вопросов"


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    question_text = models.TextField(max_length=250)

    question_choice1 = models.TextField(max_length=250)
    question_choice2 = models.TextField(max_length=250)
    question_choice3 = models.TextField(max_length=250)
    question_choice4 = models.TextField(max_length=250)

    time_to_answer = models.PositiveIntegerField()
    is_approved = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Question, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"
