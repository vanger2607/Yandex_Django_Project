# Generated by Django 3.2.16 on 2022-12-22 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0002_auto_20221222_1712'),
        ('duels', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='battle',
            options={'verbose_name': 'битва', 'verbose_name_plural': 'битвы'},
        ),
        migrations.RenameField(
            model_name='round',
            old_name='battle',
            new_name='battle_id',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='created',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='number_of_rounds',
        ),
        migrations.RemoveField(
            model_name='round',
            name='player_first',
        ),
        migrations.RemoveField(
            model_name='round',
            name='player_second',
        ),
        migrations.RemoveField(
            model_name='round',
            name='questions',
        ),
        migrations.AlterField(
            model_name='battle',
            name='is_over',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='round',
            name='is_over',
            field=models.BooleanField(default=0),
        ),
        migrations.CreateModel(
            name='PlayerAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_right', models.BooleanField(null=True)),
                ('player_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battle_player', to=settings.AUTH_USER_MODEL)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question')),
                ('round_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='duels.round')),
            ],
            options={
                'verbose_name': 'вопрос в раунде',
                'verbose_name_plural': 'вопросы в раунде',
            },
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_recieved_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_recieved', to=settings.AUTH_USER_MODEL)),
                ('player_sent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_sent', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'вызов',
                'verbose_name_plural': 'вызовы',
            },
        ),
    ]
