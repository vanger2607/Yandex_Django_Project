# Generated by Django 3.2.16 on 2022-12-21 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0004_auto_20221222_0235"),
        ("users", "0003_auto_20221220_2242"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="best_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="questions.category",
                verbose_name="лучшая категория",
            ),
        ),
    ]