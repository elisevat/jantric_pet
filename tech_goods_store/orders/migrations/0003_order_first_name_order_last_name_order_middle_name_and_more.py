# Generated by Django 5.0.6 on 2024-08-27 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_email_order_notes_order_postcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия'),
        ),
        migrations.AddField(
            model_name='order',
            name='middle_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_on_get',
            field=models.BooleanField(default=True, verbose_name='Оплата при получении'),
        ),
    ]
