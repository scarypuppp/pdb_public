# Generated by Django 3.2.7 on 2021-11-17 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('mainapp', '0021_featured'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Featured',
            new_name='FeaturedProblems',
        ),
    ]