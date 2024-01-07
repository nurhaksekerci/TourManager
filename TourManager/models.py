from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Sirket(models.Model):
    name = models.CharField(verbose_name="Adı", max_length=155)
    start = models.DateField(verbose_name="Başlama Tarihi")
    finish = models.DateField(verbose_name="Bitiş Tarihi")
    is_active = models.BooleanField(verbose_name="Aktif mi?")

    def __str__(self):
        return self.name
    
class Personel(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Aktif mi?", default=True)

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
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=155)
    city = models.CharField(verbose_name="Şehir", max_length=155)
    document_no = models.CharField(verbose_name="Rehber No", max_length=155)
    phone = models.CharField(verbose_name="Telefon No", max_length=155)
    mail = models.CharField(verbose_name="Mail", max_length=155)
    price = models.DecimalField(verbose_name="Ücreti", max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi")

    def __str__(self):
        return f"{self.city} - {self.name}"
    
class Hotel(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Adı", max_length=100)
    city = models.CharField(verbose_name="Şehir", max_length=155)
    mail = models.CharField(verbose_name="Mail", max_length=155)
    one_person = models.DecimalField(verbose_name="Tek Kişilik Ücreti", max_digits=10, decimal_places=2)
    two_person = models.DecimalField(verbose_name="İki Kişilik Ücreti", max_digits=10, decimal_places=2)
    tree_person = models.DecimalField(verbose_name="Üç Kişilik Ücreti", max_digits=10, decimal_places=2)
    finish = models.DateField(verbose_name="Fiyat Geçerlilik Tarihi")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi")

    def __str__(self):
        return f"{self.city} - {self.name}"
    
class Activity(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
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
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, verbose_name="Tedarikçi", on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, verbose_name="Tur", on_delete=models.CASCADE, blank=True, null=True)
    transfer = models.ForeignKey(Transfer, verbose_name="Transfer", on_delete=models.CASCADE, blank=True, null=True)
    car = models.DecimalField(verbose_name="Binek", max_digits=10, decimal_places=2)
    minivan = models.DecimalField(verbose_name="Minivan", max_digits=10, decimal_places=2, blank=True, null=True)
    minibus = models.DecimalField(verbose_name="Minibüs", max_digits=10, decimal_places=2, blank=True, null=True)
    midibus = models.DecimalField(verbose_name="Midibüs", max_digits=10, decimal_places=2, blank=True, null=True)
    bus = models.DecimalField(verbose_name="Otobüs", max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi")
    
    def __str__(self):
        return f"{self.supplier}"
    
class ActivityCost(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    supplier = models.ForeignKey(ActivitySupplier, verbose_name="Aktivite Tedarikçisi", on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, verbose_name="Activite", on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(verbose_name="Ücreti", max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi")
    
    def __str__(self):
        return f"{self.supplier}"

class BuyerCompany(models.Model):
    company=models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(verbose_name="Adı", max_length=100)
    short_name = models.CharField(verbose_name="Kısa adı", max_length=5)
    contact = models.CharField(verbose_name="İletişim", max_length=155)

    def __str__(self):
        return self.name
    

class Operation(models.Model):
    CURRENCY_CHOICES = (
        ('TL', 'TL'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
    company = models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    selling_staff = models.ForeignKey(Personel, verbose_name="Satan Personel", related_name="Satan", on_delete=models.CASCADE, blank=True, null=True)
    follow_staff = models.ForeignKey(Personel, verbose_name="Takip Eden Personel", related_name="Takip", on_delete=models.CASCADE)
    buyer_company = models.ForeignKey(BuyerCompany, verbose_name="Alıcı Firma", related_name="Alıcı", on_delete=models.CASCADE)
    start = models.DateField(verbose_name="Başlama Tarihi")
    finish = models.DateField(verbose_name="Bitiş Tarihi")
    create_date = models.DateTimeField(verbose_name="Oluşturulma Tarihi", auto_now=False, auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="Güncelleme Tarihi", auto_now=True, auto_now_add=False)
    passenger_info = models.TextField(verbose_name="Yolcu Bilgileri")
    ticket = models.CharField(verbose_name="Etiket", unique=True, max_length=50, blank=True, null=True)
    sales_price = models.DecimalField(verbose_name="Satış Fiyatı", max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Para Birimi", default="USD")
    number_passengers = models.PositiveIntegerField(verbose_name="Yolcu Sayısı", default=1)

    def __str__(self):
        return f"{self.ticket}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            original = Operation.objects.get(pk=self.pk)
            firma_adi_degisti = original.buyer_company.short_name != self.buyer_company.short_name
            tarih_degisti = original.start != self.start
        else:
            firma_adi_degisti = tarih_degisti = True

        if firma_adi_degisti or tarih_degisti:
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

        super().save(*args, **kwargs)
    

class OperationDay(models.Model):
    company = models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, verbose_name="Operasyon", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Tarih")

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class OperationItem(models.Model):
    OPERATIONSTYPE_CHOICES = (
        ('Karsilama', 'Karşılama'),
        ('Ugurlama', 'Uğurlama'),
        ('Tur', 'Tur'),
        ('Arac', 'Araç'),
        ('Aktivite', 'Aktivite'),
        ('Muze', 'Müze'),
        ('Otel', 'Otel'),
        ('Rehber', 'Rehber'),
        ('Aracli Rehber', 'Araçlı Rehber'),
        ('Serbest Zaman', 'Serbest Zaman'),
    )
    ROOMTYPE_CHOICES = (
        ('Tek', 'Tek'),
        ('Cift', 'Çift'),
        ('Uc', 'Üç'),
    )
    company = models.ForeignKey(Sirket, verbose_name="Sirket", on_delete=models.CASCADE)
    day = models.ForeignKey(OperationDay, verbose_name="Gün", on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=20, choices=OPERATIONSTYPE_CHOICES, verbose_name="işlem Türü")
    description = models.CharField(verbose_name="Açıklama", max_length=255, blank=True, null=True)
    tour = models.ForeignKey(Tour, verbose_name="Tur", on_delete=models.CASCADE, blank=True, null=True)
    transfer = models.ForeignKey(Transfer, verbose_name="Transfer", on_delete=models.CASCADE, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, verbose_name="Araç", on_delete=models.CASCADE, blank=True, null=True)
    guide = models.ForeignKey(Guide, verbose_name="Rehber", on_delete=models.CASCADE, blank=True, null=True)
    activity = models.ForeignKey(Activity, verbose_name="Aktivite", on_delete=models.CASCADE, blank=True, null=True)
    museum = models.ForeignKey(Museum, verbose_name="Müze", on_delete=models.CASCADE, blank=True, null=True)
    hotel = models.ForeignKey(Hotel, verbose_name="Otel", on_delete=models.CASCADE, blank=True, null=True)
    room_type = models.CharField(max_length=20, choices=ROOMTYPE_CHOICES, verbose_name="Oda Türü", blank=True, null=True)
    hotel_price = models.DecimalField(verbose_name="Otel Ücreti", max_digits=10, decimal_places=2, default=0)
    guide_price = models.DecimalField(verbose_name="Rehber Ücreti", max_digits=10, decimal_places=2, default=0)
    activity_price = models.DecimalField(verbose_name="Aktivite Ücreti", max_digits=10, decimal_places=2, default=0)
    museym_price = models.DecimalField(verbose_name="Müze Ücreti", max_digits=10, decimal_places=2, default=0)
    cost = models.ForeignKey(Cost, verbose_name="Araç Tedarikci", on_delete=models.CASCADE, blank=True, null=True)
    activity_cost = models.ForeignKey(ActivityCost, verbose_name="Aktivite Tedarikçi", on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"{self.day} - {self.operation_type}"
    