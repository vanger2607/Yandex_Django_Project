# Generated by Django 3.2.16 on 2023-01-09 19:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("duels", "0006_playeranswer_player_answer"),
    ]

    operations = [
        migrations.AddField(
            model_name="playeranswer",
            name="start_answering",
            field=models.TimeField(
                default=datetime.datetime(
                    2023, 1, 9, 19, 42, 51, 558720, tzinfo=utc
                )
            ),
            preserve_default=False,
        ),
    ]
