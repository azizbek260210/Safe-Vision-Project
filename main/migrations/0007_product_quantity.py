# Generated by Django 5.0.6 on 2024-06-07 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_banner_remove_productimg_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]