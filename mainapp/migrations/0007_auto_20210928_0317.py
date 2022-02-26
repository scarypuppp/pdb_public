# Generated by Django 3.2.7 on 2021-09-28 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20210928_0313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование раздела')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='topic',
            name='branch',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='mainapp.branch', verbose_name='Раздел'),
        ),
    ]