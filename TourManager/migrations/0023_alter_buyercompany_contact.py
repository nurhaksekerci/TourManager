# Generated by Django 4.2.9 on 2024-01-12 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TourManager", "0022_alter_cost_car_alter_cost_currency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buyercompany",
            name="contact",
            field=models.CharField(
                blank=True, max_length=155, null=True, verbose_name="İletişim"
            ),
        ),
    ]