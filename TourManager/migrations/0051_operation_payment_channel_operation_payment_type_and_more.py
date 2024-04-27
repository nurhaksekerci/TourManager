# Generated by Django 4.2.9 on 2024-03-22 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TourManager", "0050_remove_operationitem_total_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="operation",
            name="payment_channel",
            field=models.CharField(
                blank=True,
                choices=[("Havale", "Havale"), ("Xctrip", "Xctrip")],
                max_length=20,
                null=True,
                verbose_name="Ödeme Kanalı",
            ),
        ),
        migrations.AddField(
            model_name="operation",
            name="payment_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Pesin", "Peşin"),
                    ("Taksitli", "Taksitli"),
                    ("Parcalı", "Parçalı"),
                ],
                max_length=20,
                null=True,
                verbose_name="Ödeme Türü",
            ),
        ),
        migrations.AddField(
            model_name="operation",
            name="remaining_payment",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=10, verbose_name="Kalan Ödeme"
            ),
        ),
        migrations.AlterField(
            model_name="operationitem",
            name="rbm_cost_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="RMB Maliyet Fiyatı (人民币 销售价格)",
            ),
        ),
    ]
