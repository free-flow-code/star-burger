# Generated by Django 3.2.15 on 2023-08-28 19:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0049_auto_20230824_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproducts',
            name='quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='количество'),
        ),
    ]