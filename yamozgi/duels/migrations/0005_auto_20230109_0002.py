# Generated by Django 3.2.16 on 2023-01-08 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("questions", "0002_auto_20221229_1723"),
        ("duels", "0004_auto_20230108_2135"),
    ]

    operations = [
        migrations.AddField(
            model_name="battle",
            name="round_now",
            field=models.IntegerField(default=1, verbose_name="раунд сейчас"),
        ),
        migrations.AlterField(
            model_name="battle",
            name="is_over",
            field=models.BooleanField(default=0, verbose_name="окончено"),
        ),
        migrations.AlterField(
            model_name="battle",
            name="player_1",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="battle_player1",
                to=settings.AUTH_USER_MODEL,
                verbose_name="игрок 1",
            ),
        ),
        migrations.AlterField(
            model_name="battle",
            name="player_2",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="battle_player2",
                to=settings.AUTH_USER_MODEL,
                verbose_name="игрок два",
            ),
        ),
        migrations.AlterField(
            model_name="challenge",
            name="player_recieved_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="player_recieved",
                to=settings.AUTH_USER_MODEL,
                verbose_name="айди, получившего пользователя",
            ),
        ),
        migrations.AlterField(
            model_name="challenge",
            name="player_sent_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="player_sent",
                to=settings.AUTH_USER_MODEL,
                verbose_name="айди, отправившего пользователя",
            ),
        ),
        migrations.AlterField(
            model_name="playeranswer",
            name="is_right",
            field=models.BooleanField(null=True, verbose_name="верно или нет"),
        ),
        migrations.AlterField(
            model_name="playeranswer",
            name="player_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="battle_player",
                to=settings.AUTH_USER_MODEL,
                verbose_name="айди игрока",
            ),
        ),
        migrations.AlterField(
            model_name="playeranswer",
            name="question_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="questions.question",
                verbose_name="айди вопроса",
            ),
        ),
        migrations.AlterField(
            model_name="playeranswer",
            name="round_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="duels.round",
                verbose_name="айди раунда",
            ),
        ),
        migrations.AlterField(
            model_name="round",
            name="question_3",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="third_question",
                to="questions.question",
                verbose_name="третий вопрос",
            ),
        ),
    ]