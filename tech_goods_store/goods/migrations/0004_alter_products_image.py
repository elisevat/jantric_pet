# Generated by Django 5.0.6 on 2024-07-30 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_alter_products_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(blank=True, height_field=210, null=True, upload_to='goods_images/', verbose_name='Изображение', width_field=270),
        ),
    ]
