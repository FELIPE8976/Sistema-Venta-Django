# Generated by Django 5.0.2 on 2024-03-13 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0006_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrito_products',
            name='have_coupon',
            field=models.BooleanField(default=0),
        ),
    ]
