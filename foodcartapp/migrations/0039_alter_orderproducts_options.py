# Generated by Django 3.2.15 on 2023-08-06 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_auto_20230806_2049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderproducts',
            options={'verbose_name': 'элемент заказа', 'verbose_name_plural': 'элементы заказа'},
        ),
    ]
