# Generated by Django 2.2.2 on 2019-12-08 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='price',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
