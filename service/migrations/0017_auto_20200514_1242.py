# Generated by Django 3.0.5 on 2020-05-14 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0016_auto_20200514_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]