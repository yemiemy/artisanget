# Generated by Django 3.0.5 on 2020-05-26 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20200526_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='carpenter',
            field=models.BooleanField(default=False),
        ),
    ]
