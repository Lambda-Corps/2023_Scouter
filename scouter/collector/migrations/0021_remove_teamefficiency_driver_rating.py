# Generated by Django 4.1.7 on 2023-04-03 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0020_alter_robot_driver_experience'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamefficiency',
            name='driver_rating',
        ),
    ]