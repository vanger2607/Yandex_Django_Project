from django.db import models

from questions.models import Question
from users.models import CustomUser
from arena.models import Category


class Challenge(models.Model):
    player_sent_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="player_sent",
    )
    player_recieved_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="player_recieved",
    )

    class Meta:
        verbose_name = "вызов"
        verbose_name_plural = "вызовы"


class Battle(models.Model):
    player_1 = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="battle_player1",
    )
    player_2 = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="battle_player2",
    )
    is_over = models.BooleanField(default=0)

    class Meta:
        verbose_name = "битва"
        verbose_name_plural = "битвы"


class Round(models.Model):
    battle_id = models.ForeignKey(Battle, on_delete=models.CASCADE)
    is_over = models.BooleanField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "раунд"
        verbose_name_plural = "раунды"


class PlayerAnswer(models.Model):
    player_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="battle_player",
    )
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    round_id = models.ForeignKey(Round, on_delete=models.CASCADE)
    is_right = models.BooleanField(null=True)

    class Meta:
        verbose_name = "вопрос в раунде"
        verbose_name_plural = "вопросы в раунде"
