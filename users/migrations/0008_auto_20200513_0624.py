# Generated by Django 3.0.5 on 2020-05-13 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200513_0614'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='finished',
            new_name='completed',
        ),
    ]