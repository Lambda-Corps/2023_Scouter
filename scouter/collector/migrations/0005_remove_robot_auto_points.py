# Generated by Django 4.1.7 on 2023-03-14 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0004_teamefficiency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='robot',
            name='auto_points',
        ),
    ]