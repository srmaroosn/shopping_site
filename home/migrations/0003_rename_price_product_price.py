# Generated by Django 4.0.4 on 2022-05-13 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='Price',
        ),
    ]
