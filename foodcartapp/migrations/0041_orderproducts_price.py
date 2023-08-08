# Generated by Django 3.2.15 on 2023-08-07 16:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_auto_20230807_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproducts',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена'),
            preserve_default=False,
        ),
    ]
