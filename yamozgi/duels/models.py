from django.db import models
from django.utils import timezone

from core.models import CoreSave
from questions.models import Category, Question
from users.models import CustomUser


class Battle(CoreSave):
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

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Battle, self).save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Round, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "раунд"
        verbose_name_plural = "раунды"
