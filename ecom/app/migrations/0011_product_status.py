# Generated by Django 5.0.1 on 2024-02-25 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_product_availability'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('Recomended', 'Recomended'), ('Best Seller', 'Best Seller')], max_length=100, null=True),
        ),
    ]