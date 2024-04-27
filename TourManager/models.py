from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F, Case, When, DecimalField

# Create your models here.
class Sirket(models.Model):
    name = models.CharField(verbose_name="Adı", max_length=155)
    start = models.DateField(verbose_name="Başlama Tarihi")
    finish = models.DateField(verbose_name="Bitiş Tarihi")
    is_active = models.BooleanField(verbose_name="Aktif mi?")

    def __str__(self):
        return self.name

class Personel(models.Model):
    JOB_CHOICES = (
        ('Satış Personeli', 'Satış Personeli'),
        ('Operasyon Şefi', 'Operasyon Şefi'),
        ('Sistem Geliştiricisi', 'Sistem Geliştiricisi'),
        ('Yönetim', 'Yönetim'),
    )
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, related_name='personel')
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Aktif mi?", default=True)
    job = models.CharField(max_length=20, choices=JOB_CHOICES, verbose_name="Görevi", default="Satış Personeli")


    def __str__(self):
        return self.user.username


class Tour(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    route = models.CharField(verbose_name="Güzergah", max_length=155)

    def __str__(self):
        return self.route

class Transfer(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    route = models.CharField(verbose_name="Güzergah", max_length=155)

    def __str__(self):
        return self.route

class Vehicle(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    vehicle = models.CharField(verbose_name="Araçlar", max_length=155)
    capacity = models.PositiveIntegerField(verbose_name="Kapasite")

    def __str__(self):
        return self.vehicle

class Guide(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=155)
    city = models.CharField(verbose_name="Şehir", max_length=155)
    document_no = models.CharField(verbose_name="Rehber No", max_length=155, blank=True, null=True)
    phone = models.CharField(verbose_name="Telefon No", max_length=155)
    mail = models.CharField(verbose_name="Mail", max_length=155, blank=True, null=True)
    price = models.DecimalField(verbose_name="Ücreti", max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi", default="TL")

    def __str__(self):
        return f"{self.city} - {self.name}"

class Hotel(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=100)
    city = models.CharField(verbose_name="Şehir", max_length=155)
    mail = models.CharField(verbose_name="Mail", max_length=155, blank=True, null=True)
    one_person = models.DecimalField(verbose_name="Tek Kişilik Ücreti", max_digits=10, decimal_places=2, default=0)
    two_person = models.DecimalField(verbose_name="İki Kişilik Ücreti", max_digits=10, decimal_places=2, default=0)
    tree_person = models.DecimalField(verbose_name="Üç Kişilik Ücreti", max_digits=10, decimal_places=2, default=0)
    finish = models.DateField(verbose_name="Fiyat Geçerlilik Tarihi", blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi", default="TL")

    def __str__(self):
        return f"{self.name} - {self.city}"

class Activity(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )

    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=100)
    city = models.CharField(verbose_name="Şehir", max_length=155)

    def __str__(self):
        return f"{self.city} - {self.name}"

class Museum(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )

    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=100)
    city = models.CharField(verbose_name="Şehir", max_length=155)
    contact = models.CharField(verbose_name="İletişim", max_length=155)
    price = models.DecimalField(verbose_name="Ücreti", max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi")

    def __str__(self):
        return f"{self.city} - {self.name}"

class Supplier(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=100)
    contact = models.CharField(verbose_name="İletişim", max_length=155)

    def __str__(self):
        return f"{self.name}"

class ActivitySupplier(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=100)
    contact = models.CharField(verbose_name="İletişim", max_length=155)

    def __str__(self):
        return f"{self.name}"

class Cost(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, verbose_name="Tedarikçi", on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, verbose_name="Tur", on_delete=models.CASCADE, blank=True, null=True)
    transfer = models.ForeignKey(Transfer, verbose_name="Transfer", on_delete=models.CASCADE, blank=True, null=True)
    car = models.DecimalField(verbose_name="Binek", max_digits=10, decimal_places=2, blank=True, null=True)
    minivan = models.DecimalField(verbose_name="Minivan", max_digits=10, decimal_places=2, blank=True, null=True)
    minibus = models.DecimalField(verbose_name="Minibüs", max_digits=10, decimal_places=2, blank=True, null=True)
    midibus = models.DecimalField(verbose_name="Midibüs", max_digits=10, decimal_places=2, blank=True, null=True)
    bus = models.DecimalField(verbose_name="Otobüs", max_digits=10, decimal_places=2, blank=True, null=True)
    sell_car = models.DecimalField(verbose_name="Binek Satış Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    sell_minivan = models.DecimalField(verbose_name="Minivan Satış Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    sell_minibus = models.DecimalField(verbose_name="Minibüs Satış Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    sell_midibus = models.DecimalField(verbose_name="Midibüs Satış Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    sell_bus = models.DecimalField(verbose_name="Otobüs Satış Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi", default="TL")

    def __str__(self):
        if self.tour != None:
            return f"{self.tour} {self.supplier.name}"
        else:
            return f"{self.transfer} {self.supplier.name}"

class ActivityCost(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    supplier = models.ForeignKey(ActivitySupplier, verbose_name="Aktivite Tedarikçisi", on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, verbose_name="Activite", on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(verbose_name="Ücreti", max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi")

    def __str__(self):
        return f"{self.supplier} - {self.activity}"

class BuyerCompany(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(verbose_name="Adı", max_length=100)
    short_name = models.CharField(verbose_name="Kısa adı", max_length=5, unique=True)
    contact = models.CharField(verbose_name="İletişim", max_length=155, blank=True, null=True)

    def __str__(self):
        return self.name


class Operation(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ('Pesin', 'Peşin'),
        ('Taksitli', 'Taksitli'),
        ('Parcalı', 'Parçalı'),
    )
    PAYMENT_CHANNEL_CHOICES = (
        ('Havale', 'Havale'),
        ('Xctrip', 'Xctrip'),
    )
    company = models.ForeignKey(Sirket, verbose_name="Şirket (公司)", on_delete=models.CASCADE)
    selling_staff = models.ForeignKey(Personel, verbose_name="Satan Personel (销售人员)", related_name="Satan", on_delete=models.CASCADE, blank=True, null=True)
    follow_staff = models.ForeignKey(Personel, verbose_name="Takip Eden Personel (跟进员工)", related_name="Takip", on_delete=models.CASCADE)
    buyer_company = models.ForeignKey(BuyerCompany, verbose_name="Alıcı Firma (买方公司)", related_name="Alıcı", on_delete=models.CASCADE)
    start = models.DateField(verbose_name="Başlama Tarihi (开始日期)")
    finish = models.DateField(verbose_name="Bitiş Tarihi (结束日期)")
    create_date = models.DateTimeField(verbose_name="Oluşturulma Tarihi (创建日期)", auto_now=False, auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="Güncelleme Tarihi (更新日期)", auto_now=True, auto_now_add=False)
    passenger_info = models.TextField(verbose_name="Yolcu Bilgileri (乘客信息)")
    ticket = models.CharField(verbose_name="Etiket (标签)", unique=True, max_length=50, blank=True, null=True)
    usd_sales_price = models.DecimalField(verbose_name="USD Satış Fiyatı (销售价格)", max_digits=10, decimal_places=2, default=0)
    eur_sales_price = models.DecimalField(verbose_name="EUR Satış Fiyatı (销售价格)", max_digits=10, decimal_places=2, default=0)
    tl_sales_price = models.DecimalField(verbose_name="TL Satış Fiyatı (销售价格)", max_digits=10, decimal_places=2, default=0)
    rbm_sales_price = models.DecimalField(verbose_name="RBM Satış Fiyatı (人民币 销售价格)", max_digits=10, decimal_places=2, default=0)
    usd_cost_price = models.DecimalField(verbose_name="USD Maliyet Fiyatı (销售价格)", max_digits=10, decimal_places=2, default=0)
    eur_cost_price = models.DecimalField(verbose_name="EUR Maliyet Fiyatı (销售价格)", max_digits=10, decimal_places=2, default=0)
    tl_cost_price = models.DecimalField(verbose_name="TL Maliyet Fiyatı (销售价格)", max_digits=10, decimal_places=2, default=0)
    rbm_cost_price = models.DecimalField(verbose_name="RBM Maliyet Fiyatı (人民币 销售价格)", max_digits=10, decimal_places=2, default=0)
    number_passengers = models.PositiveIntegerField(verbose_name="Yolcu Sayısı (乘客数量)", default=1)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES,  blank=True, null=True, verbose_name="Ödeme Türü")
    payment_channel = models.CharField(max_length=20, choices=PAYMENT_CHANNEL_CHOICES,  blank=True, null=True, verbose_name="Ödeme Kanalı")
    remaining_payment = models.DecimalField(verbose_name="Kalan Ödeme", max_digits=10, decimal_places=2, default=0)



    def __str__(self):
        return f"{self.ticket}"



    def save(self, *args, **kwargs):
        self.calculate_and_update_total_costs()
        if not self.ticket:
            # Ticket boşsa yeni bir değer atama işlemi
            if not self.pk or self.buyer_company.short_name != Operation.objects.get(pk=self.pk).buyer_company.short_name or self.start != Operation.objects.get(pk=self.pk).start:
                kisa_ad = self.buyer_company.short_name
                tarih_format = self.start.strftime("%d%m%y")

                # Benzersiz bir etiket oluşturana kadar döngü
                tur_sayisi = 1
                while True:
                    potansiyel_etiket = f"{kisa_ad}{tarih_format}{str(tur_sayisi).zfill(3)}"
                    if not Operation.objects.filter(ticket=potansiyel_etiket).exclude(pk=self.pk).exists():
                        self.ticket = potansiyel_etiket
                        break
                    tur_sayisi += 1
        else:
            # Ticket zaten varsa, kontrol etmeden kaydet
            pass
        super().save(*args, **kwargs)

    def calculate_and_update_total_costs(self):
        # Maliyet toplamlarını başlat
        total_usd = total_eur = total_tl = total_rbm = 0

        # İlgili OperationDay nesneleri üzerinden iterate et
        operation_days = OperationDay.objects.filter(operation=self)
        for day in operation_days:
            # Her bir OperationDay için ilişkili OperationItem nesnelerini bul
            operation_items = OperationItem.objects.filter(day=day)
            for item in operation_items:
                total_usd += item.usd_cost_price
                total_eur += item.eur_cost_price
                total_tl += item.tl_cost_price
                total_rbm += item.rbm_cost_price

        # Doğrudan operation'ın maliyet alanlarını güncelle
        self.usd_cost_price = total_usd
        self.eur_cost_price = total_eur
        self.tl_cost_price = total_tl
        self.rbm_cost_price = total_rbm


class PaymentDocument(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi", default="TL")
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='payment_documents', verbose_name="İşlem")
    document = models.FileField(upload_to='payment_documents/%Y/%m/%d/', verbose_name="Dekont")
    price = models.DecimalField(verbose_name="Ödeme Miktarı", max_digits=10, decimal_places=2, default=0)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Yükleme Tarihi")

    def __str__(self):
        return f"{self.operation.ticket} - {self.document.name}"

class SupplierPaymentDocument(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi", default="TL")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='payment_documents', verbose_name="Tedarikci")
    document = models.FileField(verbose_name="Dekont", upload_to='payment_documents/%Y/%m/%d/', blank=True, null=True)
    price = models.DecimalField(verbose_name="Ödeme Miktarı", max_digits=10, decimal_places=2, default=0)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Yükleme Tarihi")

    def __str__(self):
        return f"{self.supplier} - {self.document.name}"

class ActivitySupplierPaymentDocument(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB (人民币)'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi", default="TL")
    supplier = models.ForeignKey(ActivitySupplier, on_delete=models.CASCADE, related_name='payment_documents', verbose_name="Tedarikci")
    document = models.FileField(verbose_name="Dekont", upload_to='payment_documents/%Y/%m/%d/', blank=True, null=True)
    price = models.DecimalField(verbose_name="Ödeme Miktarı", max_digits=10, decimal_places=2, default=0)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Yükleme Tarihi")

    def __str__(self):
        return f"{self.supplier} - {self.document.name}"



class OperationDay(models.Model):
    company = models.ForeignKey(Sirket, verbose_name="Şirket (公司)", on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, verbose_name="Operasyon (操作)", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Tarih (日期)")

    def __str__(self):
        return self.date.strftime("%d-%m-%Y")


from django.db.models.signals import post_save
from django.dispatch import receiver

class OperationItem(models.Model):
    OPERATIONSTYPE_CHOICES = (
        ('Karsilama', 'Karşılama (迎接)'),
        ('Ugurlama', 'Uğurlama (送别)'),
        ('Tur', 'Tur (旅游)'),
        ('TurTransfer', 'Tur + Transfer'),
        ('TransferTur', 'Transfer + Tur'),
        ('Arac', 'Araç (车辆)'),
        ('Aktivite', 'Aktivite (活动)'),
        ('Muze', 'Müze (博物馆)'),
        ('Otel', 'Otel (酒店)'),
        ('Rehber', 'Rehber (导游)'),
        ('Aracli Rehber', 'Araçlı Rehber (带车导游)'),
        ('Serbest Zaman', 'Serbest Zaman (自由时间)'),
    )
    ROOMTYPE_CHOICES = (
        ('Tek', 'Tek (单人)'),
        ('Cift', 'Çift (双人)'),
        ('Uc', 'Üç (三人)'),
    )
    CURRENCY_CHOICES = (
        ('TL', 'TL (土耳其里拉)'),
        ('USD', 'USD (美元)'),
        ('EUR', 'EUR (欧元)'),
        ('RMB', 'RMB (人民币)'),
    )
    company = models.ForeignKey(Sirket, verbose_name="Şirket (公司)", on_delete=models.CASCADE)
    day = models.ForeignKey(OperationDay, verbose_name="Gün (日)", on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=20, choices=OPERATIONSTYPE_CHOICES, verbose_name="İşlem Türü (操作类型)")
    pick_time = models.TimeField(blank=True, null=True, verbose_name="Alış Saati (接载时间)")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Açıklama (描述)")
    tour = models.ForeignKey(Tour, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Tur (旅游)")
    transfer = models.ForeignKey(Transfer, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Transfer (转移)")
    vehicle = models.ForeignKey(Vehicle, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Araç (车辆)")
    guide = models.ForeignKey(Guide, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Rehber (导游)")
    activity = models.ForeignKey(Activity, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Aktivite (活动)")
    museum = models.ForeignKey(Museum, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Müze (博物馆)", related_name="old_operation_items")
    hotel = models.ForeignKey(Hotel, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Otel (酒店)")
    room_type = models.CharField(max_length=20, choices=ROOMTYPE_CHOICES, blank=True, null=True, verbose_name="Oda Türü (房间类型)")
    hotel_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Otel Ücreti (酒店价格)")
    hotel_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Otel Para Birimi (货币)", default="USD")
    guide_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Rehber Ücreti (导游费)")
    guide_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Rehber Para Birimi (货币)", default="USD")
    activity_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Aktivite Ücreti (活动费)")
    activity_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Aktivite Para Birimi (货币)", default="USD")
    museym_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Müze Ücreti (博物馆费用)")
    museum_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Müze Para Birimi (货币)", default="USD")
    other_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Diğer Ücretler")
    other_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Diğer Ücretler Para Birimi", default="USD")
    activity_cost = models.ForeignKey(ActivitySupplier, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Aktivite Tedarikçi (活动供应商)")
    cost = models.ForeignKey(Cost, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Araç Maaliyet (车辆供应商)")
    driver = models.CharField(max_length=255, blank=True, null=True, verbose_name="Şoför (司机)")
    driver_phone = models.CharField(max_length=255, blank=True, null=True, verbose_name="Şoför Telefon (司机电话)")
    plaka = models.CharField(max_length=255, blank=True, null=True, verbose_name="Plaka (牌照号码是)")
    supplier = models.ForeignKey(Supplier, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Araç Tedarikçi (车辆供应商)")
    vehicle_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Araç Ücreti")
    usd_cost_price = models.DecimalField(verbose_name="USD Maliyet Fiyatı (销售价格)", max_digits=10, decimal_places=2, default=0)
    eur_cost_price = models.DecimalField(verbose_name="EUR Maliyet Fiyatı (销售价格)", max_digits=10, decimal_places=2, default=0)
    tl_cost_price = models.DecimalField(verbose_name="TL Maliyet Fiyatı (销售价格)", max_digits=10, decimal_places=2, default=0)
    rbm_cost_price = models.DecimalField(verbose_name="RMB Maliyet Fiyatı (人民币 销售价格)", max_digits=10, decimal_places=2, default=0)
    new_museum = models.ManyToManyField(Museum, blank=True, verbose_name="Müzeler (博物馆)", related_name="new_operation_items")


    def __str__(self):
        return f"{self.day} - {self.operation_type}"


    def save(self, *args, **kwargs):
        # Yeni kayıt olup olmadığını kontrol et
        is_new = not self.pk
        # Eğer yeni bir kayıt değilse, supplier alanındaki değişikliği kontrol et
        supplier_changed = False
        if not is_new:
            prev_instance = OperationItem.objects.get(pk=self.pk)
            supplier_changed = prev_instance.supplier != self.supplier

        # Modelin orijinal save metodunu çağır
        super().save(*args, **kwargs)


        self.calculate_and_update_costs()

    def calculate_and_update_costs(self):
        # Para birimlerine göre toplam maliyetleri hesapla
        total_costs = self.calculate_total_costs_by_currency()

        # Hesaplanan maliyetleri ilgili para birimi değişkenlerine ata
        self.usd_cost_price = total_costs.get('USD', 0)
        self.eur_cost_price = total_costs.get('EUR', 0)
        self.tl_cost_price = total_costs.get('TL', 0)
        self.rbm_cost_price = total_costs.get('RMB', 0)
        total_costs['TL'] += self.vehicle_price
        # Güncellenen alanları kaydet
        super(OperationItem, self).save(update_fields=['usd_cost_price', 'eur_cost_price', 'tl_cost_price', 'rbm_cost_price'])

    def calculate_total_costs_by_currency(self):
        # Para birimlerine göre toplam maliyetleri başlangıçta 0 olarak ayarla
        total_costs = {
            'USD': 0,
            'EUR': 0,
            'TL': 0,
            'RMB': 0,
        }

        # Otel maliyetini ilgili para birimi toplamına ekle
        if self.hotel_currency in total_costs:
            total_costs[self.hotel_currency] += self.hotel_price

        # Rehber maliyetini ilgili para birimi toplamına ekle
        if self.guide_currency in total_costs:
            total_costs[self.guide_currency] += self.guide_price

        # Aktivite maliyetini ilgili para birimi toplamına ekle
        if self.activity_currency in total_costs:
            total_costs[self.activity_currency] += self.activity_price

        # Müze maliyetini ilgili para birimi toplamına ekle
        if self.museum_currency in total_costs:
            total_costs[self.museum_currency] += self.museym_price

        # Diğer maliyetleri ilgili para birimi toplamlarına ekle
        if self.other_currency in total_costs:
            total_costs[self.other_currency] += self.other_price

        # Araç maliyetini ilgili para birimi toplamına ekle
        # Not: Araç maliyeti için varsayılan para birimi TL olarak kabul edilmiştir.
        total_costs['TL'] += self.vehicle_price

        return total_costs


class Fiyatlandırma(models.Model):
    sirket = models.ForeignKey(Sirket, verbose_name="Şirket", on_delete=models.CASCADE, blank=True, null=True)
    olusturan = models.ForeignKey(Personel, verbose_name="Personel", on_delete=models.CASCADE, blank=True, null=True)
    genel_toplam = models.DecimalField(verbose_name="Genel Toplam Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    arac_toplam = models.DecimalField(verbose_name="Araç Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    transfer_toplam = models.DecimalField(verbose_name="Transfer Toplam Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    rehber_toplam = models.DecimalField(verbose_name="Rehber Toplam Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    yemek_toplam = models.DecimalField(verbose_name="Yemek Toplam Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    double_oda_toplam = models.DecimalField(verbose_name="Double Oda Toplam Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    single_oda_toplam = models.DecimalField(verbose_name="Single Oda Toplam Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    onay = models.BooleanField(verbose_name="Onay", default=False)
    islem = models.BooleanField(verbose_name="İslem", default=False)
    aciklama = models.TextField(verbose_name="Açıklama", default="Beklemede")
    def __str__(self):
        return f"{self.olusturan} - {self.genel_toplam}"

    class Meta:
        verbose_name = "Fiyatlandırma"
        verbose_name_plural = "Fiyatlandırmalar"

class FiyatlandirmaItem(models.Model):
    sirket = models.ForeignKey(Sirket, verbose_name="Şirket", on_delete=models.CASCADE, blank=True, null=True)
    fiyat = models.ForeignKey(Fiyatlandırma, verbose_name="Fiyatlandırma", on_delete=models.CASCADE)
    tarih = models.DateField(verbose_name="Tarih", blank=True, null=True)
    aciklama = models.CharField(verbose_name="Açıklama", max_length=50, blank=True, null=True)
    arac_fiyati = models.DecimalField(verbose_name="Araç Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    transfer_fiyati = models.DecimalField(verbose_name="Transfer Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    rehber_fiyati = models.DecimalField(verbose_name="Rehber Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    yemek_fiyati = models.DecimalField(verbose_name="Yemek Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    double_oda_fiyati = models.DecimalField(verbose_name="Double Oda Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)
    single_oda_fiyati = models.DecimalField(verbose_name="Single Oda Fiyatı", max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.fiyat.olusturan.user.get_full_name()} - {self.tarih}"

    class Meta:
        verbose_name = "Fiyatlandırma Item"
        verbose_name_plural = "Fiyatlandırma Itemleri"



class UserActivityLog(models.Model):
    company = models.ForeignKey(Sirket, verbose_name="Şirket (公司)", on_delete=models.CASCADE, blank=True, null=True)
    staff = models.ForeignKey(Personel, verbose_name="Personel", on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff} - {self.action} - {self.timestamp}"
