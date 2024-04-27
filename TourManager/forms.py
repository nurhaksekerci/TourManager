from django import forms
from .models import *
from django.forms import inlineformset_factory

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle', 'capacity']
        widgets = {
            'vehicle': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['route',]
        widgets = {
            'route': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['route',]
        widgets = {
            'route': forms.TextInput(attrs={'class': 'form-control'}),
        }


class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['name', 'city', 'document_no', 'phone', 'mail', 'price', 'currency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'document_no': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'city', 'mail', 'one_person', 'two_person', 'tree_person', 'finish', 'currency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'one_person': forms.NumberInput(attrs={'class': 'form-control'}),
            'two_person': forms.NumberInput(attrs={'class': 'form-control'}),
            'tree_person': forms.NumberInput(attrs={'class': 'form-control'}),
            'finish': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MuseumForm(forms.ModelForm):
    class Meta:
        model = Museum
        fields = ['name', 'city', 'contact', 'price', 'currency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }

from django.contrib.auth.models import User
class PersonelForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Personel
        fields = ['is_active', 'job']
        widgets = {
            'job': forms.Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance and instance.user:
            initial = kwargs.get('initial', {})
            initial['first_name'] = instance.user.first_name
            initial['last_name'] = instance.user.last_name
            initial['email'] = instance.user.email
            initial['username'] = instance.user.username
            kwargs['initial'] = initial
        super(PersonelForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user_data = {
            'first_name': self.cleaned_data.get('first_name'),
            'last_name': self.cleaned_data.get('last_name'),
            'email': self.cleaned_data.get('email'),
            'username': self.cleaned_data.get('username'),
        }

        personel_is_active = self.cleaned_data.get('is_active')

        if self.instance.pk:
            # Güncelleme
            user = self.instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            if self.cleaned_data.get('password'):
                # Şifre alanı doldurulmuşsa, şifreyi de güncelle
                user.set_password(self.cleaned_data.get('password'))
            # Personel modelindeki is_active alanını User modeline eşitle
            user.is_active = personel_is_active
            user.save()
        else:
            # Yeni Kullanıcı
            user_password = self.cleaned_data.get('password')
            user = User.objects.create_user(**user_data, password=user_password or 'default_password')
            # Personel modelindeki is_active alanını User modeline eşitle
            user.is_active = personel_is_active
            self.instance.user = user

        if commit:
            self.instance.save()
        return self.instance

class CostForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['supplier', 'tour', 'transfer', 'car', 'minivan', 'minibus', 'midibus', 'bus', 'currency', 'sell_car', 'sell_minivan', 'sell_minibus', 'sell_midibus', 'sell_bus']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'tour': forms.Select(attrs={'class': 'form-control'}),
            'transfer': forms.Select(attrs={'class': 'form-control'}),
            'car': forms.NumberInput(attrs={'class': 'form-control'}),
            'minivan': forms.NumberInput(attrs={'class': 'form-control'}),
            'minibus': forms.NumberInput(attrs={'class': 'form-control'}),
            'midibus': forms.NumberInput(attrs={'class': 'form-control'}),
            'bus': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'sell_car': forms.NumberInput(attrs={'class': 'form-control'}),
            'sell_minivan': forms.NumberInput(attrs={'class': 'form-control'}),
            'sell_minibus': forms.NumberInput(attrs={'class': 'form-control'}),
            'sell_midibus': forms.NumberInput(attrs={'class': 'form-control'}),
            'sell_bus': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ActivitySupplierForm(forms.ModelForm):
    class Meta:
        model = ActivitySupplier
        fields = ['name', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BuyerCompanyForm(forms.ModelForm):
    class Meta:
        model = BuyerCompany
        fields = ['name', 'short_name', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['follow_staff', 'buyer_company', 'ticket', 'start', 'finish', 'usd_sales_price', 'eur_sales_price', 'tl_sales_price', 'rbm_sales_price', 'passenger_info', 'number_passengers', 'payment_channel', 'payment_type']
        widgets = {
            'follow_staff': forms.Select(attrs={'class': 'form-control'}),
            'buyer_company': forms.Select(attrs={'class': 'form-control'}),
            'payment_type': forms.Select(attrs={'class': 'form-control'}),
            'payment_channel': forms.Select(attrs={'class': 'form-control'}),
            'start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'finish': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'passenger_info': forms.Textarea(attrs={'class': 'form-control'}),
            'ticket': forms.TextInput(attrs={'class': 'form-control'}),
            'usd_sales_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'eur_sales_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tl_sales_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'rbm_sales_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),

            'number_passengers': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class SupplierPaymentDocumentForm(forms.ModelForm):
    class Meta:
        model = SupplierPaymentDocument
        fields = ['price', 'currency', 'document']
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}),

        }


class PaymentDocumentForm(forms.ModelForm):
    class Meta:
        model = PaymentDocument
        fields = ['price', 'currency', 'document']
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}),
        }


class ActivitySupplierPaymentDocumentForm(forms.ModelForm):
    class Meta:
        model = ActivitySupplierPaymentDocument
        fields = ['price', 'currency', 'document']
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}),
        }

class OperationDayForm(forms.ModelForm):
    class Meta:
        model = OperationDay
        fields = ['date',]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class OperationItemForm(forms.ModelForm):
    class Meta:
        model = OperationItem
        fields = [
            'operation_type', 'description', 'pick_time', 'tour', 'transfer', 'vehicle',
            'guide', 'activity', 'hotel', 'room_type', 'hotel_price',
            'guide_price', 'activity_price', 'museym_price', 'new_museum', 'other_price', 'supplier', 'vehicle_price', 'activity_cost', 'hotel_currency', 'guide_currency', 'activity_currency', 'other_currency', 'museum_currency', 'activity_cost', 'cost', 'driver', 'driver_phone', 'plaka'
        ]
        widgets = {
            'operation_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'driver': forms.TextInput(attrs={'class': 'form-control'}),
            'driver_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'plaka': forms.TextInput(attrs={'class': 'form-control'}),
            'pick_time': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
            'tour': forms.Select(attrs={'class': 'form-control'}),
            'transfer': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'guide': forms.Select(attrs={'class': 'form-control'}),
            'activity': forms.Select(attrs={'class': 'form-control'}),
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'hotel_currency': forms.Select(attrs={'class': 'form-control'}),
            'guide_currency': forms.Select(attrs={'class': 'form-control'}),
            'activity_currency': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'activity_cost': forms.Select(attrs={'class': 'form-control'}),
            'museum_currency': forms.Select(attrs={'class': 'form-control'}),
            'other_currency': forms.Select(attrs={'class': 'form-control'}),
            'hotel_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'other_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'guide_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'activity_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'museym_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'vehicle_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'new_museum': forms.SelectMultiple(attrs={'class': 'form-control'}),


        }
    def __init__(self, *args, **kwargs):
        super(OperationItemForm, self).__init__(*args, **kwargs)
        # 'guide' alanı için alfabetik sıralama
        self.fields['guide'].queryset = self.fields['guide'].queryset.order_by('city')
        # 'activity' alanı için alfabetik sıralama
        self.fields['activity'].queryset = self.fields['activity'].queryset.order_by('city')
        self.fields['tour'].queryset = self.fields['tour'].queryset.order_by('route')
        self.fields['transfer'].queryset = self.fields['transfer'].queryset.order_by('route')
        self.fields['new_museum'].queryset = self.fields['new_museum'].queryset.order_by('city')
        self.fields['hotel'].queryset = self.fields['hotel'].queryset.order_by('city')
        self.fields['supplier'].queryset = self.fields['supplier'].queryset.order_by('name')
        self.fields['activity_cost'].queryset = self.fields['activity_cost'].queryset.order_by('name')
        # Diğer Select alanları için benzer sıralamalar yapılabilir

class CostAddVehicleForm(forms.ModelForm):
    class Meta:
        model = OperationItem
        fields = ['supplier', 'vehicle_price']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'vehicle_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }



class CostAddHotelForm(forms.ModelForm):
    class Meta:
        model = OperationItem
        fields = ['hotel', 'room_type', 'hotel_price', 'hotel_currency']
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'hotel_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'hotel_currency': forms.Select(attrs={'class': 'form-control'}),
        }


class CostAddGuideForm(forms.ModelForm):
    class Meta:
        model = OperationItem
        fields = ['guide', 'guide_price', 'guide_currency']
        widgets = {
            'guide': forms.Select(attrs={'class': 'form-control'}),
            'guide_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'guide_currency': forms.Select(attrs={'class': 'form-control'}),
        }

class CostAddActivityForm(forms.ModelForm):
    class Meta:
        model = OperationItem
        fields = ['activity_cost', 'activity_price', 'activity_currency']
        widgets = {
            'activity_cost': forms.Select(attrs={'class': 'form-control'}),
            'activity_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'activity_currency': forms.Select(attrs={'class': 'form-control'}),
        }

class CostAddMuseumForm(forms.ModelForm):
    class Meta:
        model = OperationItem
        fields = ['museym_price', 'museum_currency']
        widgets = {
            'museym_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'museum_currency': forms.Select(attrs={'class': 'form-control'}),
        }
class DriverForm(forms.ModelForm):  # Formunuzun adını buraya yazın
    class Meta:
        model = OperationItem  # Modelinizin adını buraya yazın
        fields = ['driver', 'driver_phone', 'plaka']
        widgets = {
            'driver': forms.TextInput(attrs={'class': 'form-control'}),
            'driver_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'plaka': forms.TextInput(attrs={'class': 'form-control'}),
        }

class WidgetMixin:
    def set_widgets(self):
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class FiyatlandirmaForm(WidgetMixin,forms.ModelForm):
    class Meta:
        model = Fiyatlandırma
        fields = ['genel_toplam', 'arac_toplam', 'transfer_toplam', 'rehber_toplam', 'yemek_toplam', 'double_oda_toplam', 'single_oda_toplam']

    genel_toplam = forms.DecimalField(label='Genel Toplam', widget=forms.TextInput(attrs={'class': 'form-control'}))
    arac_toplam = forms.DecimalField(label='Araç Toplam', widget=forms.TextInput(attrs={'class': 'form-control'}))
    transfer_toplam = forms.DecimalField(label='Transfer Toplam', widget=forms.TextInput(attrs={'class': 'form-control'}))
    rehber_toplam = forms.DecimalField(label='Rehber Toplam', widget=forms.TextInput(attrs={'class': 'form-control'}))
    yemek_toplam = forms.DecimalField(label='Yemek Toplam', widget=forms.TextInput(attrs={'class': 'form-control'}))
    double_oda_toplam = forms.DecimalField(label='Double Oda Toplam', widget=forms.TextInput(attrs={'class': 'form-control'}))
    single_oda_toplam = forms.DecimalField(label='Single Oda Toplam', widget=forms.TextInput(attrs={'class': 'form-control'}))


from django import forms
from django.forms.widgets import TextInput

class FiyatlandirmaItemForm(WidgetMixin, forms.ModelForm):
    tarih = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'class': 'form-control', 'placeholder': 'gg.aa.yyyy'}),
        label='Tarih'
    )
    class Meta:
        model = FiyatlandirmaItem
        fields = ['tarih', 'aciklama', 'arac_fiyati', 'transfer_fiyati', 'rehber_fiyati', 'yemek_fiyati', 'double_oda_fiyati', 'single_oda_fiyati']
        labels = {
            'tarih': 'Tarih',
            'aciklama': 'Açıklama',
            'arac_fiyati': 'Araç Fiyatı',
            'transfer_fiyati': 'Transfer Fiyatı',
            'rehber_fiyati': 'Rehber Fiyatı',
            'yemek_fiyati': 'Yemek Fiyatı',
            'double_oda_fiyati': 'Double Oda Fiyatı',
            'single_oda_fiyati': 'Single Oda Fiyatı',
        }
        widgets = {
            'tarih': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'gg.aa.yyyy'}),
            'aciklama': forms.TextInput(attrs={'class': 'form-control'}),
            'arac_fiyati': forms.TextInput(attrs={'class': 'form-control'}),
            'transfer_fiyati': forms.TextInput(attrs={'class': 'form-control'}),
            'rehber_fiyati': forms.TextInput(attrs={'class': 'form-control'}),
            'yemek_fiyati': forms.TextInput(attrs={'class': 'form-control'}),
            'double_oda_fiyati': forms.TextInput(attrs={'class': 'form-control'}),
            'single_oda_fiyati': forms.TextInput(attrs={'class': 'form-control'}),
        }

        input_formats = {
            'tarih': ['%d.%m.%Y'],
        }


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FiyatlandirmaItemForm, self).__init__(*args, **kwargs)
        self.set_widgets()


# Satis modeli için SatisItem formseti oluştur
FiyatlandirmaItemFormSet = inlineformset_factory(Fiyatlandırma, FiyatlandirmaItem, form=FiyatlandirmaItemForm, extra=15)

