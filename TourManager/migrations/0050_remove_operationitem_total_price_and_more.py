# Generated by Django 4.2.9 on 2024-02-07 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TourManager", "0049_operationitem_total_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="operationitem",
            name="total_price",
        ),
        migrations.AddField(
            model_name="operation",
            name="eur_cost_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="EUR Maliyet Fiyatı (销售价格)",
            ),
        ),
        migrations.AddField(
            model_name="operation",
            name="rbm_cost_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="RBM Maliyet Fiyatı (人民币 销售价格)",
            ),
        ),
        migrations.AddField(
            model_name="operation",
            name="tl_cost_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="TL Maliyet Fiyatı (销售价格)",
            ),
        ),
        migrations.AddField(
            model_name="operation",
            name="usd_cost_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="USD Maliyet Fiyatı (销售价格)",
            ),
        ),
        migrations.AddField(
            model_name="operationitem",
            name="eur_cost_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="EUR Maliyet Fiyatı (销售价格)",
            ),
        ),
        migrations.AddField(
            model_name="operationitem",
            name="rbm_cost_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="RBM Maliyet Fiyatı (人民币 销售价格)",
            ),
        ),
        migrations.AddField(
            model_name="operationitem",
            name="tl_cost_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="TL Maliyet Fiyatı (销售价格)",
            ),
        ),
        migrations.AddField(
            model_name="operationitem",
            name="usd_cost_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="USD Maliyet Fiyatı (销售价格)",
            ),
        ),
    ]