from django import forms
from .models import *

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
        fields = ['is_active']

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
        fields = ['supplier', 'tour', 'transfer', 'car', 'minivan', 'minibus', 'midibus', 'bus', 'currency']
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
        fields = ['follow_staff', 'buyer_company', 'start', 'finish', 'currency', 'sales_price', 'passenger_info', 'number_passengers']
        widgets = {
            'follow_staff': forms.Select(attrs={'class': 'form-control'}),
            'buyer_company': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'finish': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'passenger_info': forms.Textarea(attrs={'class': 'form-control'}),
            'passenger_info': forms.Textarea(attrs={'class': 'form-control'}),
            'sales_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'number_passengers': forms.NumberInput(attrs={'class': 'form-control'}),
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
            'operation_type', 'description', 'tour', 'transfer', 'vehicle', 
            'guide', 'activity', 'museum', 'hotel', 'room_type', 'hotel_price', 
            'guide_price', 'activity_price', 'museym_price', 'cost', 'activity_cost'
        ]
        widgets = {
            'operation_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'tour': forms.Select(attrs={'class': 'form-control'}),
            'transfer': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'guide': forms.Select(attrs={'class': 'form-control'}),
            'activity': forms.Select(attrs={'class': 'form-control'}),
            'museum': forms.Select(attrs={'class': 'form-control'}),
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'hotel_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'guide_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'activity_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'museym_price': forms.NumberInput(attrs={'class': 'form-control'})
        }

class CostAddVehicleForm(forms.ModelForm):
    class Meta:
        model = OperationItem
        fields = ['cost',]
        widgets = {
            'cost': forms.Select(attrs={'class': 'form-control'}),
        }



class CostAddHotelForm(forms.ModelForm):
    class Meta:
        model = OperationItem
        fields = ['hotel', 'room_type', 'hotel_price']
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'hotel_price': forms.NumberInput(attrs={'class': 'form-control'})
        }


class CostAddGuideForm(forms.ModelForm):
    class Meta:
        model = OperationItem
        fields = ['guide', 'guide_price']
        widgets = {
            'guide': forms.Select(attrs={'class': 'form-control'}),
            'guide_price': forms.NumberInput(attrs={'class': 'form-control'})
        }

class CostAddActivityForm(forms.ModelForm):
    class Meta:
        model = OperationItem
        fields = ['activity_cost', 'activity_price']
        widgets = {
            'activity_cost': forms.Select(attrs={'class': 'form-control'}),
            'activity_price': forms.NumberInput(attrs={'class': 'form-control'})
        }

class CostAddMuseumForm(forms.ModelForm):
    class Meta:
        model = OperationItem
        fields = ['museym_price',]
        widgets = {
            'museym_price': forms.NumberInput(attrs={'class': 'form-control'})
        }