# Generated by Django 4.2.9 on 2024-01-25 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TourManager", "0044_operationitem_vehicle_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="operationitem",
            name="other_currency",
            field=models.CharField(
                choices=[
                    ("TL", "TL (土耳其里拉)"),
                    ("USD", "USD (美元)"),
                    ("EUR", "EUR (欧元)"),
                    ("RMB", "RMB (人民币)"),
                ],
                default="USD",
                max_length=3,
                verbose_name="Diğer Ücretler Para Birimi",
            ),
        ),
        migrations.AddField(
            model_name="operationitem",
            name="other_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="Diğer Ücretler",
            ),
        ),
    ]
