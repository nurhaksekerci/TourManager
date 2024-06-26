# Generated by Django 4.2.9 on 2024-01-19 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("TourManager", "0039_rename_fiyatlandirma_fiyatlandırma"),
    ]

    operations = [
        migrations.CreateModel(
            name="Fiyatlandirma",
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
                ("start", models.DateField(verbose_name="Başlama Tarihi (开始日期)")),
                ("finish", models.DateField(verbose_name="Bitiş Tarihi (结束日期)")),
                (
                    "genel_toplam",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Genel Toplam Fiyatı",
                    ),
                ),
                (
                    "arac_toplam",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Araç Fiyatı",
                    ),
                ),
                (
                    "transfer_toplam",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Transfer Toplam Fiyatı",
                    ),
                ),
                (
                    "rehber_toplam",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Rehber Toplam Fiyatı",
                    ),
                ),
                (
                    "yemek_toplam",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Yemek Toplam Fiyatı",
                    ),
                ),
                (
                    "double_oda_toplam",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Double Oda Toplam Fiyatı",
                    ),
                ),
                (
                    "single_oda_toplam",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Single Oda Toplam Fiyatı",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="TourManager.sirket",
                        verbose_name="Şirket",
                    ),
                ),
                (
                    "create_staff",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="TourManager.personel",
                        verbose_name="Personel",
                    ),
                ),
            ],
            options={
                "verbose_name": "Fiyatlandırma",
                "verbose_name_plural": "Fiyatlandırmalar",
            },
        ),
        migrations.AlterField(
            model_name="fiyatlandirmaitem",
            name="fiyat",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="TourManager.fiyatlandirma",
                verbose_name="Fiyatlandırma",
            ),
        ),
        migrations.DeleteModel(
            name="Fiyatlandırma",
        ),
    ]
