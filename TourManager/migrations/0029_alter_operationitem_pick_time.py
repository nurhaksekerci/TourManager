# Generated by Django 4.2.9 on 2024-01-14 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TourManager", "0028_alter_operationitem_pick_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="operationitem",
            name="pick_time",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Alış Saati (接载时间)"
            ),
        ),
    ]