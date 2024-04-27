# Generated by Django 4.2.9 on 2024-02-07 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TourManager", "0048_cost_sell_bus_cost_sell_car_cost_sell_midibus_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="operationitem",
            name="total_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="Toplam Maliyet",
            ),
        ),
    ]