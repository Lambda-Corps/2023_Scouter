# Generated by Django 4.1.7 on 2023-03-11 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0002_matchresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchresult',
            name='match_number',
            field=models.IntegerField(default=0),
        ),
    ]
