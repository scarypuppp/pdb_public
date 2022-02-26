# Generated by Django 3.2.7 on 2021-10-12 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0012_auto_20210929_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='problem',
            name='with_image',
            field=models.BooleanField(default=False, verbose_name='Задача с картинкой'),
        ),
    ]
