# Generated by Django 3.2.16 on 2022-12-22 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20221222_1712'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='null', upload_to='uploads/%Y/%m', verbose_name='аватар'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='best_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='questions.category', verbose_name='лучшая категория'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='count_of_battles',
            field=models.IntegerField(blank=True, null=True, verbose_name='количество битв'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='count_of_questions',
            field=models.IntegerField(blank=True, null=True, verbose_name='количество созданных вопросов'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='count_of_wins',
            field=models.IntegerField(blank=True, null=True, verbose_name='количество побед'),
        ),
    ]
