# Generated by Django 5.0.6 on 2024-07-18 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_subs_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_birth',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Дата рождения'),
        ),
    ]
