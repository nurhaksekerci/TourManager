# Generated by Django 4.2.9 on 2024-01-15 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TourManager", "0029_alter_operationitem_pick_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="operationitem",
            name="driver_phone",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                verbose_name="Şoför Telefon (司机电话)",
            ),
        ),
    ]
