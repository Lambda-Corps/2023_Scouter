# Generated by Django 4.1.7 on 2023-03-24 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0015_rename_auto_cones_high_matchresult_auto_high_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='robot',
            name='game_pieces',
        ),
        migrations.RemoveField(
            model_name='robot',
            name='preffered_grid',
        ),
        migrations.AddField(
            model_name='robot',
            name='driver_experience',
            field=models.IntegerField(default=0, max_length=1),
        ),
    ]
