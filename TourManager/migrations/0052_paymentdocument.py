# Generated by Django 4.2.9 on 2024-03-22 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "TourManager",
            "0051_operation_payment_channel_operation_payment_type_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "document",
                    models.FileField(
                        upload_to="payment_documents/%Y/%m/%d/", verbose_name="Dekont"
                    ),
                ),
                (
                    "upload_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yükleme Tarihi"
                    ),
                ),
                (
                    "operation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment_documents",
                        to="TourManager.operation",
                        verbose_name="İşlem",
                    ),
                ),
            ],
        ),
    ]
