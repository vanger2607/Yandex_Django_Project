# Generated by Django 3.2.16 on 2022-12-21 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("duels", "0002_alter_round_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="battle",
            name="created",
        ),
        migrations.RemoveField(
            model_name="battle",
            name="modified",
        ),
    ]
