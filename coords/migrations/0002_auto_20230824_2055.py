# Generated by Django 3.2.15 on 2023-08-24 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coords', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='place',
            name='lat',
            field=models.FloatField(null=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='place',
            name='lon',
            field=models.FloatField(null=True, verbose_name='Долгота'),
        ),
    ]