# Generated by Django 2.2.2 on 2020-01-07 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0009_auto_20191208_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
