# Generated by Django 3.2.16 on 2022-12-21 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0004_auto_20221222_0235"),
        ("duels", "0004_auto_20221221_2351"),
    ]

    operations = [
        migrations.AlterField(
            model_name="round",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="questions.category",
            ),
        ),
    ]
