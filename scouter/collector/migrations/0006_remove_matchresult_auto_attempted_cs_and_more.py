# Generated by Django 4.1.7 on 2023-03-15 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0005_remove_robot_auto_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchresult',
            name='auto_attempted_cs',
        ),
        migrations.RemoveField(
            model_name='matchresult',
            name='auto_scored',
        ),
        migrations.RemoveField(
            model_name='matchresult',
            name='tele_attempted',
        ),
        migrations.RemoveField(
            model_name='matchresult',
            name='tele_links',
        ),
        migrations.RemoveField(
            model_name='matchresult',
            name='tele_scored',
        ),
    ]
