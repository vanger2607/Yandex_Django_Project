# Generated by Django 3.2.16 on 2023-01-18 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_customuser_login"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="gray_matter",
            field=models.IntegerField(
                default=0, verbose_name="серое вещество"
            ),
        ),
    ]
