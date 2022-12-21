from django.db import models

from questions.models import Question
from users.models import CustomUser
from arena.models import Category


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
    number_of_rounds = models.PositiveSmallIntegerField()
    is_over = models.BooleanField()

    class Meta:
        verbose_name = "поединок"
        verbose_name_plural = "поединки"


class Round(models.Model):
    player_first = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="first_turn_player",
    )
    player_second = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="second_turn_player",
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    is_over = models.BooleanField()
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "раунд"
        verbose_name_plural = "раунды"
