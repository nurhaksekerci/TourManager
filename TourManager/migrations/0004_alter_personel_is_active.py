# Generated by Django 4.2.9 on 2024-01-06 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0003_museum_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personel',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Aktif mi?'),
        ),
    ]