# Generated by Django 4.2.9 on 2024-01-07 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0014_alter_operation_selling_staff_alter_operation_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationitem',
            name='activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TourManager.activity', verbose_name='Aktivite'),
        ),
        migrations.AlterField(
            model_name='operationitem',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Açıklama'),
        ),
        migrations.AlterField(
            model_name='operationitem',
            name='guide',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TourManager.guide', verbose_name='Rehber'),
        ),
        migrations.AlterField(
            model_name='operationitem',
            name='hotel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TourManager.hotel', verbose_name='Otel'),
        ),
        migrations.AlterField(
            model_name='operationitem',
            name='museum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TourManager.museum', verbose_name='Müze'),
        ),
        migrations.AlterField(
            model_name='operationitem',
            name='room_type',
            field=models.CharField(blank=True, choices=[('Tek', 'Tek'), ('Cift', 'Çift'), ('Uc', 'Üç')], max_length=20, null=True, verbose_name='Oda Türü'),
        ),
        migrations.AlterField(
            model_name='operationitem',
            name='tour',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TourManager.tour', verbose_name='Tur'),
        ),
        migrations.AlterField(
            model_name='operationitem',
            name='transfer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TourManager.transfer', verbose_name='Transfer'),
        ),
        migrations.AlterField(
            model_name='operationitem',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TourManager.vehicle', verbose_name='Araç'),
        ),
    ]