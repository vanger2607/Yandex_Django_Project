# Generated by Django 3.2.16 on 2022-12-21 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("arena", "0002_auto_20221221_1901"),
        ("duels", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="round",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="arena.category",
            ),
        ),
    ]
