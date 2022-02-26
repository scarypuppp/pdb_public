# Generated by Django 3.2.7 on 2021-11-17 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0022_rename_featured_featuredproblems'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='views_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='featuredproblems',
            name='problems',
            field=models.ManyToManyField(blank=True, related_name='related_featured', to='mainapp.Problem'),
        ),
    ]