# Generated by Django 3.2.16 on 2023-01-08 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0002_auto_20221229_1723"),
        ("duels", "0002_auto_20221229_1723"),
    ]

    operations = [
        migrations.AlterField(
            model_name="round",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="questions.category",
            ),
        ),
    ]
