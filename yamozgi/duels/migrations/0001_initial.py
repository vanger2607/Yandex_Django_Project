# Generated by Django 3.2.16 on 2022-12-15 18:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("questions", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Battle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number_of_rounds", models.PositiveSmallIntegerField()),
                ("is_over", models.BooleanField()),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                (
                    "player_1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="battle_player1",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "player_2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="battle_player2",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "поединок",
                "verbose_name_plural": "поединки",
            },
        ),
        migrations.CreateModel(
            name="Round",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_over", models.BooleanField()),
                (
                    "battle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="duels.battle"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="questions.category",
                    ),
                ),
                (
                    "player_first",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="first_turn_player",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "player_second",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="second_turn_player",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("questions", models.ManyToManyField(to="questions.Question")),
            ],
            options={
                "verbose_name": "раунд",
                "verbose_name_plural": "раунды",
            },
        ),
    ]
