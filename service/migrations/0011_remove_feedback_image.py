# Generated by Django 2.2.2 on 2020-01-07 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0010_feedback_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='image',
        ),
    ]
