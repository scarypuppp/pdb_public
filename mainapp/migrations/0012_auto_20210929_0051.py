# Generated by Django 3.2.7 on 2021-09-28 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20210929_0020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='title',
        ),
    ]