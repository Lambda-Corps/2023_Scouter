# Generated by Django 4.1.7 on 2023-03-26 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0016_remove_robot_game_pieces_remove_robot_preffered_grid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamefficiency',
            name='penalty_rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
