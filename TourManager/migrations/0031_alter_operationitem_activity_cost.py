# Generated by Django 4.2.9 on 2024-01-15 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("TourManager", "0030_operationitem_driver_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="operationitem",
            name="activity_cost",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="TourManager.activitysupplier",
                verbose_name="Aktivite Tedarikçi (活动供应商)",
            ),
        ),
    ]
