# Generated by Django 3.2.7 on 2021-09-28 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20210928_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='with_image',
            field=models.BooleanField(default=False, verbose_name='Задача с картинкой'),
        ),
    ]
