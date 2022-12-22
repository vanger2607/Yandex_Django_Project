# Generated by Django 3.2.16 on 2022-12-21 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0003_delete_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name": "категория вопроса",
                "verbose_name_plural": "категории вопросов",
            },
        ),
        migrations.AlterField(
            model_name="question",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="questions.category",
            ),
        ),
    ]
