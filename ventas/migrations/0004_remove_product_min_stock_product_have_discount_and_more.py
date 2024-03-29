# Generated by Django 5.0.2 on 2024-03-08 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0003_product_min_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='min_stock',
        ),
        migrations.AddField(
            model_name='product',
            name='have_discount',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
