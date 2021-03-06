# Generated by Django 3.2.7 on 2021-11-23 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0028_problem_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название коллекции')),
                ('solve_time', models.DurationField()),
                ('problems', models.ManyToManyField(to='mainapp.Problem', verbose_name='Задачи')),
            ],
        ),
    ]
