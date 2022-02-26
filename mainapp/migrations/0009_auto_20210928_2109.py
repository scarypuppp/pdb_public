# Generated by Django 3.2.7 on 2021-09-28 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_problem_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='extended_answer',
            field=models.BooleanField(default=False, verbose_name='Развернутый ответ'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='answer',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ответ'),
        ),
    ]