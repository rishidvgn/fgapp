# Generated by Django 3.1.4 on 2020-12-29 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fgapp', '0008_todayfg_old'),
    ]

    operations = [
        migrations.AddField(
            model_name='todayfg_old',
            name='kam_des_advice',
            field=models.TextField(default='No'),
        ),
    ]
