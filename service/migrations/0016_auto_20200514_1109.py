# Generated by Django 3.0.5 on 2020-05-14 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0015_remove_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='area',
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='Lagos', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(default='Lagos', max_length=120),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Area',
        ),
    ]
