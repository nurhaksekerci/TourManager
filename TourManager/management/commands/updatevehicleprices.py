# myapp/management/commands/updatevehicleprices.py
from django.core.management.base import BaseCommand
from TourManager.models import OperationItem, Cost, Vehicle

class Command(BaseCommand):
    help = 'Updates vehicle prices in OperationItem from matching Cost records'

    def handle(self, *args, **options):
        for operation_item in OperationItem.objects.filter(vehicle_price=0, supplier__id=16):  # Düzeltildi
            tour = operation_item.tour
            transfer = operation_item.transfer
            supplier = operation_item.supplier
            vehicle_type = operation_item.vehicle.vehicle  # Burada vehicle_type'ı nasıl belirleyeceğinize karar vermelisiniz.
            plaka = operation_item.plaka
            birlestirilmis_arac = Vehicle.objects.get(id=123)
            # Eşleşen Cost kaydını bul
            cost_query = Cost.objects.filter(supplier=supplier)
            if tour:
                cost_query = cost_query.filter(tour=tour)
            if transfer:
                cost_query = cost_query.filter(transfer=transfer)

            # Eşleşen kayıtlardan birini seç (örneğin, ilkini)
            cost = cost_query.first()
            if cost:
                # Maliyeti hesapla ve kaydet
                if vehicle_type == 'Binek':
                    operation_item.vehicle_price = cost.car if cost.car else 0
                if vehicle_type == 'Minivan':
                    operation_item.vehicle_price = cost.minivan if cost.minivan else 0
                if vehicle_type == 'Minibüs':
                    operation_item.vehicle_price = cost.minibus if cost.minibus else 0
                if vehicle_type == 'Midibüs':
                    operation_item.vehicle_price = cost.midibus if cost.midibus else 0
                if vehicle_type == 'Otobüs':
                    operation_item.vehicle_price = cost.bus if cost.bus else 0
                if vehicle_type == 'Birleştirme':
                    operation_item.vehicle_price = 0

                operation_item.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated vehicle prices.'))


