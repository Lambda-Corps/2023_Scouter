# Generated by Django 4.1.7 on 2023-03-27 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0017_teamefficiency_penalty_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamefficiency',
            name='total_points',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
