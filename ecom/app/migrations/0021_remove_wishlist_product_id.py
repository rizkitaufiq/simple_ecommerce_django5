# Generated by Django 5.0.1 on 2024-03-02 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_wishlist_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product_id',
        ),
    ]
