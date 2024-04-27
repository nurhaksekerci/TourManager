from django.core.management.base import BaseCommand
from TourManager.models import OperationItem  # Uygun model yollarınızı kullanın

class Command(BaseCommand):
    help = 'Museum alanındaki kayıtları new_museum alanına aktarır'

    def handle(self, *args, **kwargs):
        # Tüm OperationItem öğelerini sorgula
        operation_items = OperationItem.objects.filter(supplier__id = 7)

        for operation_item in operation_items:
            if operation_item.vehicle_price == 0:
                car = operation_item.vehicle.vehicle
                if operation_item.tour:
                    tour = operation_item.tour
                    cost = Cost.objects.filter(tour = tour, supplier__id = 7).first()
                    if car == "BINEK":
                        cost_vehicle_price = cost.car
                        operation_item.vehicle_price = cost_vehicle_price
                    if car == "MINIVAN":
                        cost_vehicle_price = cost.minivan
                        operation_item.vehicle_price = cost_vehicle_price
                    if car == "MINIBÜS":
                        cost_vehicle_price = cost.minibus
                        operation_item.vehicle_price = cost_vehicle_price
                    if car = "MIDIBÜS":
                        cost_vehicle_price = cost.midibus
                        operation_item.vehicle_price = cost_vehicle_price
                    if car = "OTOBÜS":
                        cost_vehicle_price = cost.bus
                        operation_item.vehicle_price = cost_vehicle_price
                    if car == "BIRLEŞTIRME"
                        operation_item.vehicle_price = 0
                    
                else:
                    transfer = operation_item.transfer
                    cost = Cost.objects.filter(transfer = transfer, supplier__id = 7).first()
                    if car == "BINEK":
                        cost_vehicle_price = cost.car
                        operation_item.vehicle_price = cost_vehicle_price
                    if car == "MINIVAN":
                        cost_vehicle_price = cost.minivan
                        operation_item.vehicle_price = cost_vehicle_price
                    if car == "MINIBÜS":
                        cost_vehicle_price = cost.minibus
                        operation_item.vehicle_price = cost_vehicle_price
                    if car = "MIDIBÜS":
                        cost_vehicle_price = cost.midibus
                        operation_item.vehicle_price = cost_vehicle_price
                    if car = "OTOBÜS":
                        cost_vehicle_price = cost.bus
                        operation_item.vehicle_price = cost_vehicle_price
                    if car == "BIRLEŞTIRME"
                        operation_item.vehicle_price = 0

        # Sonuç mesajını yazdır
        self.stdout.write(self.style.SUCCESS(f'Toplam {total_count} adet OperationItem güncellendi.'))

