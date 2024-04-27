# Generated by Django 4.2.9 on 2024-01-15 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "TourManager",
            "0032_alter_activitycost_currency_alter_cost_currency_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="operationitem",
            name="activity_currency",
            field=models.CharField(
                choices=[
                    ("TL", "TL (土耳其里拉)"),
                    ("USD", "USD (美元)"),
                    ("EUR", "EUR (欧元)"),
                    ("RMB", "RMB (人民币)"),
                ],
                default="USD",
                max_length=3,
                verbose_name="Aktivite Para Birimi (货币)",
            ),
        ),
        migrations.AddField(
            model_name="operationitem",
            name="guide_currency",
            field=models.CharField(
                choices=[
                    ("TL", "TL (土耳其里拉)"),
                    ("USD", "USD (美元)"),
                    ("EUR", "EUR (欧元)"),
                    ("RMB", "RMB (人民币)"),
                ],
                default="USD",
                max_length=3,
                verbose_name="Rehber Para Birimi (货币)",
            ),
        ),
        migrations.AddField(
            model_name="operationitem",
            name="hotel_currency",
            field=models.CharField(
                choices=[
                    ("TL", "TL (土耳其里拉)"),
                    ("USD", "USD (美元)"),
                    ("EUR", "EUR (欧元)"),
                    ("RMB", "RMB (人民币)"),
                ],
                default="USD",
                max_length=3,
                verbose_name="Otel Para Birimi (货币)",
            ),
        ),
        migrations.AddField(
            model_name="operationitem",
            name="museum_currency",
            field=models.CharField(
                choices=[
                    ("TL", "TL (土耳其里拉)"),
                    ("USD", "USD (美元)"),
                    ("EUR", "EUR (欧元)"),
                    ("RMB", "RMB (人民币)"),
                ],
                default="USD",
                max_length=3,
                verbose_name="Müze Para Birimi (货币)",
            ),
        ),
    ]