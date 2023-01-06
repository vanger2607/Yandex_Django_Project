from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "категория вопроса"
        verbose_name_plural = "категории вопросов"

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    author = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
    )
    question_text = models.TextField(max_length=250)

    question_choice1 = models.TextField(max_length=250)
    question_choice2 = models.TextField(max_length=250)
    question_choice3 = models.TextField(max_length=250)
    question_choice4 = models.TextField(max_length=250)

    right_answer = models.CharField(
        null=False,
        blank=False,
        verbose_name="правильный ответ",
        max_length=100,
    )
    difficulty = models.IntegerField(default=0)

    is_approved = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"
