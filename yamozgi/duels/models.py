from django.db import models

from questions.models import Question
from users.models import CustomUser
from questions.models import Category


class Challenge(models.Model):
    player_sent_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="player_sent",
        verbose_name="айди, отправившего пользователя",
    )
    player_recieved_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="player_recieved",
        verbose_name="айди, получившего пользователя",
    )

    class Meta:
        verbose_name = "вызов"
        verbose_name_plural = "вызовы"


class Battle(models.Model):
    player_1 = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="battle_player1",
        verbose_name="игрок 1",
    )
    player_2 = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="battle_player2",
        verbose_name="игрок два",
    )
    is_over = models.BooleanField(
        default=0,
        verbose_name="окончено",
    )
    round_now = models.IntegerField(
        default=1,
        verbose_name="раунд сейчас",
    )
    player_1_scores = models.IntegerField(
        default=0,
        verbose_name="очки первого игрока",
    )
    player_2_scores = models.IntegerField(
        default=0,
        verbose_name="очки второго игрока",
    )

    class Meta:
        verbose_name = "битва"
        verbose_name_plural = "битвы"


class Round(models.Model):
    battle_id = models.ForeignKey(
        Battle,
        on_delete=models.CASCADE,
        verbose_name="айди битвы",
    )
    is_over = models.BooleanField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="категория",
    )
    question_1 = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="первый вопрос",
        related_name="first_question",
    )
    question_2 = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="второй вопрос",
        related_name="second_question",
    )
    question_3 = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="третий вопрос",
        related_name="third_question",
    )

    class Meta:
        verbose_name = "раунд"
        verbose_name_plural = "раунды"


class PlayerAnswer(models.Model):
    player_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="battle_player",
        verbose_name="айди игрока",
    )
    question_id = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="айди вопроса",
    )
    round_id = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        verbose_name="айди раунда",
    )
    is_right = models.BooleanField(
        null=True,
        verbose_name="верно или нет",
    )
    player_answer = models.CharField(
        verbose_name="ответ игрока",
        max_length=150,
    )
    start_answering = models.TimeField()

    class Meta:
        verbose_name = "вопрос в раунде"
        verbose_name_plural = "вопросы в раунде"
