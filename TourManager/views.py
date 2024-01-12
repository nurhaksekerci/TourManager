from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.forms.models import model_to_dict

from .forms import *
from .models import *
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Call Django's login function
            return redirect('vehicle')  # Redirect to a success page.
        else:
            return render(request, 'tour/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'tour/login.html')
def logout(request):
    auth_logout(request)
    return redirect('login')  # Redirect to a login page.


def transfer(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        'title' : 'Transfer',
        'createtitle' : 'Transfer Oluştur',
        'listTitle' : 'Transfer Listesi',
        'createUrl' : 'create_transfer',
        'deleteUrl' : 'delete_transfer',
        'form' : TransferForm(),
        'transfers' : Transfer.objects.filter(company = sirket)

    }

    return render(request, 'tour/transfer.html', context)

def create_transfer(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = TransferForm(request.POST or None)
        if form.is_valid():
            new_transfer = form.save(commit=False)
            new_transfer.company = sirket
            new_transfer.save()
            context = {
                'createUrl' : 'create_transfer',
                'deleteUrl' : 'delete_transfer',
                'transfer' : new_transfer
            }
            return render(request, 'tour/partials/transfer-list.html', context)

    context={
        'createUrl' : 'create_transfer',
        'deleteUrl' : 'delete_transfer',
        'form' : TransferForm()    
    }

    return render(request, 'tour/partials/transfer-form.html', context)
from django.http import HttpResponse

def delete_transfer(request, transfer_id):
    if request.method == "DELETE":
        transfer = get_object_or_404(Transfer, id=transfer_id)
        transfer.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


def edit_transfer(request, transfer_id):
    transfer = get_object_or_404(Transfer, id=transfer_id)

    if request.method == "POST":
        form = TransferForm(request.POST, instance=transfer)
        if form.is_valid():
            form.save()
            return render(request, 'tour/partials/transfer-list.html', {'form': form, 'transfer': transfer})

    else:
        form = TransferForm(instance=transfer)

    return render(request, 'tour/partials/transfer-edit-form.html', {'form': form, 'transfer': transfer})

def cancel_transfer(request, transfer_id):
    # İlgili firma nesnesini al
    transfer = get_object_or_404(Transfer, id=transfer_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/transfer-list.html', {'transfer': transfer})


def tour(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        'title' : 'Tur',
        'createtitle' : 'Tur Oluştur',
        'listTitle' : 'Tur Listesi',
        'createUrl' : 'create_tour',
        'deleteUrl' : 'delete_tour',
        'form' : TourForm(),
        'tours' : Tour.objects.filter(company = sirket)

    }

    return render(request, 'tour/tour.html', context)

def create_tour(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = TourForm(request.POST or None)
        if form.is_valid():
            new_tour = form.save(commit=False)
            new_tour.company = sirket
            new_tour.save()
            context = {
                'createUrl' : 'create_tour',
                'deleteUrl' : 'delete_tour',
                'tour' : new_tour
            }
            return render(request, 'tour/partials/tour-list.html', context)

    context={
        'createUrl' : 'create_tour',
        'deleteUrl' : 'delete_tour',
        'form' : TourForm()    
    }

    return render(request, 'tour/partials/tour-form.html', context)
from django.http import HttpResponse

def delete_tour(request, tour_id):
    if request.method == "DELETE":
        tour = get_object_or_404(Tour, id=tour_id)
        tour.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == "POST":
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            return render(request, 'tour/partials/tour-list.html', {'form': form, 'tour': tour})

    else:
        form = TourForm(instance=tour)

    return render(request, 'tour/partials/tour-edit-form.html', {'form': form, 'tour': tour})

def cancel_tour(request, tour_id):
    # İlgili firma nesnesini al
    tour = get_object_or_404(Tour, id=tour_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/tour-list.html', {'tour': tour})




def vehicle(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        'title': 'Araç (车辆)',
        'createtitle': 'Araç Oluştur (创建车辆)',
        'listTitle': 'Araçlar Listesi (车辆列表)',
        'createUrl' : 'create_vehicle',
        'deleteUrl' : 'delete_vehicle',
        'form' : VehicleForm(),
        'vehicles' : Vehicle.objects.filter(company = sirket)

    }

    return render(request, 'tour/vehicle.html', context)

def create_vehicle(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = VehicleForm(request.POST or None)
        if form.is_valid():
            new_vehicle = form.save(commit=False)
            new_vehicle.company = sirket
            new_vehicle.save()
            context = {
                'createUrl' : 'create_vehicle',
                'deleteUrl' : 'delete_vehicle',
                'vehicle' : new_vehicle
            }
            return render(request, 'tour/partials/vehicle-list.html', context)

    context={
        'createUrl' : 'create_vehicle',
        'deleteUrl' : 'delete_vehicle',
        'form' : VehicleForm()    
    }

    return render(request, 'tour/partials/vehicle-form.html', context)
from django.http import HttpResponse

def delete_vehicle(request, vehicle_id):
    if request.method == "DELETE":
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        vehicle.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return render(request, 'tour/partials/vehicle-list.html', {'form': form, 'vehicle': vehicle})

    else:
        form = VehicleForm(instance=vehicle)

    return render(request, 'tour/partials/vehicle-edit-form.html', {'form': form, 'vehicle': vehicle})

def cancel_vehicle(request, vehicle_id):
    # İlgili firma nesnesini al
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/vehicle-list.html', {'vehicle': vehicle})



def guide(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        'title' : 'Rehber',
        'createtitle' : 'Rehber Oluştur',
        'listTitle' : 'Rehber Listesi',
        'createUrl' : 'create_guide',
        'deleteUrl' : 'delete_guide',
        'form' : GuideForm(),
        'guides' : Guide.objects.filter(company = sirket)

    }

    return render(request, 'tour/guide.html', context)

def create_guide(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = GuideForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            context = {
                'createUrl' : 'create_guide',
                'deleteUrl' : 'delete_guide',
                'guide' : new
            }
            return render(request, 'tour/partials/guide-list.html', context)

    context={
        'createUrl' : 'create_guide',
        'deleteUrl' : 'delete_guide',
        'form' : GuideForm()    
    }

    return render(request, 'tour/partials/guide-form.html', context)
from django.http import HttpResponse

def delete_guide(request, guide_id):
    if request.method == "DELETE":
        guide = get_object_or_404(Guide, id=guide_id)
        guide.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


def edit_guide(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id)

    if request.method == "POST":
        form = GuideForm(request.POST, instance=guide)
        if form.is_valid():
            form.save()
            return render(request, 'tour/partials/guide-list.html', {'form': form, 'guide': guide})

    else:
        form = GuideForm(instance=guide)

    return render(request, 'tour/partials/guide-edit-form.html', {'form': form, 'guide': guide})

def cancel_guide(request, guide_id):
    # İlgili firma nesnesini al
    guide = get_object_or_404(Guide, id=guide_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/guide-list.html', {'guide': guide})



def hotel(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        'title' : 'Otel',
        'createtitle' : 'Otel Oluştur',
        'listTitle' : 'Otel Listesi',
        'createUrl' : 'create_hotel',
        'deleteUrl' : 'delete_hotel',
        'form' : HotelForm(),
        'hotels' : Hotel.objects.filter(company = sirket)

    }

    return render(request, 'tour/hotel.html', context)

def create_hotel(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = HotelForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            context = {
                'createUrl' : 'create_hotel',
                'deleteUrl' : 'delete_hotel',
                'hotel' : new
            }
            return render(request, 'tour/partials/hotel-list.html', context)

    context={
        'createUrl' : 'create_hotel',
        'deleteUrl' : 'delete_hotel',
        'form' : HotelForm()    
    }

    return render(request, 'tour/partials/hotel-form.html', context)
from django.http import HttpResponse

def delete_hotel(request, hotel_id):
    if request.method == "DELETE":
        hotel = get_object_or_404(Hotel, id=hotel_id)
        hotel.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


def edit_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == "POST":
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return render(request, 'tour/partials/hotel-list.html', {'form': form, 'hotel': hotel})

    else:
        form = HotelForm(instance=hotel)

    return render(request, 'tour/partials/hotel-edit-form.html', {'form': form, 'hotel': hotel})

def cancel_hotel(request, hotel_id):
    # İlgili firma nesnesini al
    hotel = get_object_or_404(Hotel, id=hotel_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/hotel-list.html', {'hotel': hotel})



def activity(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        'title' : 'Aktivite',
        'createtitle' : 'Aktivite Oluştur',
        'listTitle' : 'Aktivite Listesi',
        'createUrl' : 'create_activity',
        'deleteUrl' : 'delete_activity',
        'form' : ActivityForm(),
        'activities' : Activity.objects.filter(company = sirket)

    }

    return render(request, 'tour/activity.html', context)

def create_activity(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = ActivityForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            context = {
                'createUrl' : 'create_activity',
                'deleteUrl' : 'delete_activity',
                'activity' : new
            }
            return render(request, 'tour/partials/activity-list.html', context)

    context={
        'createUrl' : 'create_activity',
        'deleteUrl' : 'delete_activity',
        'form' : ActivityForm()    
    }

    return render(request, 'tour/partials/activity-form.html', context)
from django.http import HttpResponse

def delete_activity(request, activity_id):
    if request.method == "DELETE":
        activity = get_object_or_404(Activity, id=activity_id)
        activity.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return render(request, 'tour/partials/activity-list.html', {'form': form, 'activity': activity})

    else:
        form = ActivityForm(instance=activity)

    return render(request, 'tour/partials/activity-edit-form.html', {'form': form, 'activity': activity})

def cancel_activity(request, activity_id):
    # İlgili firma nesnesini al
    activity = get_object_or_404(Activity, id=activity_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/activity-list.html', {'activity': activity})



def personel(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        'title' : 'Personel',
        'createtitle' : 'Personel Oluştur',
        'listTitle' : 'Personel Listesi',
        'createUrl' : 'create_personel',
        'deleteUrl' : 'delete_personel',
        'form' : PersonelForm(),
        'personels' : Personel.objects.filter(company = sirket)

    }

    return render(request, 'tour/personel.html', context)

def create_personel(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = PersonelForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            context = {
                'createUrl' : 'create_personel',
                'deleteUrl' : 'delete_personel',
                'personel' : new
            }
            return render(request, 'tour/partials/personel-list.html', context)

    context={
        'createUrl' : 'create_personel',
        'deleteUrl' : 'delete_personel',
        'form' : PersonelForm()    
    }

    return render(request, 'tour/partials/personel-form.html', context)
from django.http import HttpResponse

def delete_personel(request, personel_id):
    if request.method == "DELETE":
        personel = get_object_or_404(Personel, id=personel_id)
        
        # İlişkili User modelini de sil
        if personel.user:
            personel.user.delete()

        personel.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


def edit_personel(request, personel_id):
    personel = get_object_or_404(Personel, id=personel_id)

    if request.method == "POST":
        form = PersonelForm(request.POST, instance=personel)
        if form.is_valid():
            form.save()
            return render(request, 'tour/partials/personel-list.html', {'form': form, 'personel': personel})
        else:
            print(form.errors)
    else:
        form = PersonelForm(instance=personel)

    return render(request, 'tour/partials/personel-edit-form.html', {'form': form, 'personel': personel})

def cancel_personel(request, personel_id):
    # İlgili firma nesnesini al
    personel = get_object_or_404(Personel, id=personel_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/personel-list.html', {'personel': personel})



def supplier(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        'title' : 'Araç Tedarikçi',
        'createtitle' : 'Araç Tedarikçi Oluştur',
        'listTitle' : 'Araç Tedarikçi Listesi',
        'createUrl' : 'create_supplier',
        'deleteUrl' : 'delete_supplier',
        'form' : SupplierForm(),
        'suppliers' : Supplier.objects.filter(company = sirket)

    }

    return render(request, 'tour/supplier.html', context)

def create_supplier(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = SupplierForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            context = {
                'createUrl' : 'create_supplier',
                'deleteUrl' : 'delete_supplier',
                'supplier' : new
            }
            return render(request, 'tour/partials/supplier-list.html', context)

    context={
        'createUrl' : 'create_supplier',
        'deleteUrl' : 'delete_supplier',
        'form' : SupplierForm()    
    }

    return render(request, 'tour/partials/supplier-form.html', context)
from django.http import HttpResponse

def delete_supplier(request, supplier_id):
    if request.method == "DELETE":
        supplier = get_object_or_404(Supplier, id=supplier_id)
        supplier.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return render(request, 'tour/partials/supplier-list.html', {'form': form, 'supplier': supplier})

    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'tour/partials/supplier-edit-form.html', {'form': form, 'supplier': supplier})

def cancel_supplier(request, supplier_id):
    # İlgili firma nesnesini al
    supplier = get_object_or_404(Supplier, id=supplier_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/supplier-list.html', {'supplier': supplier})


def activity_supplier(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        'title' : 'Aktivite Tedarikçi',
        'createtitle' : 'Aktivite Tedarikçi Oluştur',
        'listTitle' : 'Aktivite Tedarikçi Listesi',
        'createUrl' : 'create_activity_supplier',
        'deleteUrl' : 'delete_activity_supplier',
        'form' : ActivitySupplierForm(),
        'activitysuppliers' : ActivitySupplier.objects.filter(company = sirket)

    }

    return render(request, 'tour/activity-supplier.html', context)

def create_activity_supplier(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = ActivitySupplierForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            context = {
                'createUrl' : 'create_activity_supplier',
                'deleteUrl' : 'delete_activity_supplier',
                'activitysupplier' : new
            }
            return render(request, 'tour/partials/activity-supplier-list.html', context)

    context={
        'createUrl' : 'create_activity_supplier',
        'deleteUrl' : 'delete_activity_supplier',
        'form' : ActivitySupplierForm()    
    }

    return render(request, 'tour/partials/activity-supplier-form.html', context)
from django.http import HttpResponse

def delete_activity_supplier(request, supplier_id):
    if request.method == "DELETE":
        supplier = get_object_or_404(ActivitySupplier, id=supplier_id)
        supplier.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


def edit_activity_supplier(request, supplier_id):
    activitysupplier = get_object_or_404(ActivitySupplier, id=supplier_id)

    if request.method == "POST":
        form = ActivitySupplierForm(request.POST, instance=activitysupplier)
        if form.is_valid():
            form.save()
            return render(request, 'tour/partials/activity-supplier-list.html', {'form': form, 'activitysupplier': activitysupplier})

    else:
        form = ActivitySupplierForm(instance=activitysupplier)

    return render(request, 'tour/partials/activity-supplier-edit-form.html', {'form': form, 'activitysupplier': activitysupplier})

def cancel_activity_supplier(request, supplier_id):
    # İlgili firma nesnesini al
    supplier = get_object_or_404(ActivitySupplier, id=supplier_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/supplier-list.html', {'supplier': supplier})


def cost(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        'title' : 'Maaliyet',
        'createtitle' : 'Maaliyet Oluştur',
        'listTitle' : 'Maaliyet Listesi',
        'createUrl' : 'create_cost',
        'deleteUrl' : 'delete_cost',
        'form' : CostForm(),
        'costs' : Cost.objects.filter(company = sirket)

    }

    return render(request, 'tour/cost.html', context)

def create_cost(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = CostForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            context = {
                'createUrl' : 'create_cost',
                'deleteUrl' : 'delete_cost',
                'cost' : new
            }
            return render(request, 'tour/partials/cost-list.html', context)

    context={
        'createUrl' : 'create_cost',
        'deleteUrl' : 'delete_cost',
        'form' : CostForm()    
    }

    return render(request, 'tour/partials/cost-form.html', context)
from django.http import HttpResponse

def delete_cost(request, cost_id):
    if request.method == "DELETE":
        cost = get_object_or_404(Cost, id=cost_id)
        cost.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


def edit_cost(request, cost_id):
    cost = get_object_or_404(Cost, id=cost_id)

    if request.method == "POST":
        form = CostForm(request.POST, instance=cost)
        if form.is_valid():
            form.save()
            return render(request, 'tour/partials/cost-list.html', {'form': form, 'cost': cost})

    else:
        form = CostForm(instance=cost)

    return render(request, 'tour/partials/cost-edit-form.html', {'form': form, 'cost': cost})

def cancel_cost(request, cost_id):
    # İlgili firma nesnesini al
    cost = get_object_or_404(Cost, id=cost_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/cost-list.html', {'cost': cost})



def museum(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        'title' : 'Müze',
        'createtitle' : 'Müze Oluştur',
        'listTitle' : 'Müze Listesi',
        'createUrl' : 'create_museum',
        'deleteUrl' : 'delete_museum',
        'form' : MuseumForm(),
        'activities' : Museum.objects.filter(company = sirket)

    }

    return render(request, 'tour/museum.html', context)

def create_museum(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = MuseumForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            context = {
                'createUrl' : 'create_museum',
                'deleteUrl' : 'delete_museum',
                'museum' : new
            }
            return render(request, 'tour/partials/museum-list.html', context)

    context={
        'createUrl' : 'create_museum',
        'deleteUrl' : 'delete_museum',
        'form' : MuseumForm()    
    }

    return render(request, 'tour/partials/museum-form.html', context)
from django.http import HttpResponse

def delete_museum(request, museum_id):
    if request.method == "DELETE":
        museum = get_object_or_404(Museum, id=museum_id)
        museum.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


def edit_museum(request, museum_id):
    museum = get_object_or_404(Museum, id=museum_id)

    if request.method == "POST":
        form = MuseumForm(request.POST, instance=museum)
        if form.is_valid():
            form.save()
            return render(request, 'tour/partials/museum-list.html', {'form': form, 'museum': museum})

    else:
        form = MuseumForm(instance=museum)

    return render(request, 'tour/partials/museum-edit-form.html', {'form': form, 'museum': museum})

def cancel_museum(request, museum_id):
    # İlgili firma nesnesini al
    museum = get_object_or_404(Museum, id=museum_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/museum-list.html', {'museum': museum})


def buyer(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        'title' : 'Firma',
        'createtitle' : 'Firma Oluştur',
        'listTitle' : 'Firma Listesi',
        'createUrl' : 'create_buyer',
        'deleteUrl' : 'delete_buyer',
        'form' : BuyerCompanyForm(),
        'buyers' : BuyerCompany.objects.filter(company = sirket)

    }

    return render(request, 'tour/buyer.html', context)

def create_buyer(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = BuyerCompanyForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            context = {
                'createUrl' : 'create_buyer',
                'deleteUrl' : 'delete_buyer',
                'buyer' : new
            }
            return render(request, 'tour/partials/buyer-list.html', context)

    context={
        'createUrl' : 'create_buyer',
        'deleteUrl' : 'delete_buyer',
        'form' : BuyerCompanyForm()    
    }

    return render(request, 'tour/partials/buyer-form.html', context)
from django.http import HttpResponse

def delete_buyer(request, buyer_id):
    if request.method == "DELETE":
        buyer = get_object_or_404(BuyerCompany, id=buyer_id)
        buyer.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


def edit_buyer(request, buyer_id):
    buyer = get_object_or_404(BuyerCompany, id=buyer_id)

    if request.method == "POST":
        form = BuyerCompanyForm(request.POST, instance=buyer)
        if form.is_valid():
            form.save()
            return render(request, 'tour/partials/buyer-list.html', {'form': form, 'buyer': buyer})

    else:
        form = BuyerCompanyForm(instance=buyer)

    return render(request, 'tour/partials/buyer-edit-form.html', {'form': form, 'buyer': buyer})

def cancel_buyer(request, buyer_id):
    # İlgili firma nesnesini al
    buyer = get_object_or_404(BuyerCompany, id=buyer_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/buyer-list.html', {'buyer': buyer})



def operation(request):
    requestPersonel = Personel.objects.get(user = request.user)
    sirket = requestPersonel.company
    
    context={
        
        'title': 'Operasyon Kur (操作设置)',
        'createtitle': 'Operasyon Oluştur (创建操作)',
        'createUrl' : 'create_operation',
        'deleteUrl' : 'delete_buyer',
        'form' : OperationForm(),
        'formgun' : OperationDayForm(),
        'formitem' : OperationItemForm(),
        

    }

    return render(request, 'tour/operation.html', context)

def create_operation(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user = request.user)
        sirket = requestPersonel.company
        form = OperationForm(request.POST or None)
        if form.is_valid():
            operasyon = form.save(commit=False)
            operasyon.selling_staff = requestPersonel
            operasyon.company = sirket
            operasyon.save()
            baslangic_tarihi = operasyon.start
            bitis_tarihi = operasyon.finish

            gun_sayisi = (bitis_tarihi - baslangic_tarihi).days
            for i in range(gun_sayisi + 1):
                gun = baslangic_tarihi + timedelta(days=i)
                operasyon_gun_form = OperationDayForm({'date': gun})
                if operasyon_gun_form.is_valid():
                    operasyon_gun = operasyon_gun_form.save(commit=False)
                    operasyon_gun.operation = operasyon
                    operasyon_gun.company = sirket
                    operasyon_gun.save()

            context = {
                'operasyon': operasyon,
                'days' : OperationDay.objects.filter(company=sirket, operation=operasyon),
                'formitem' : OperationItemForm()
            }
            return render(request, 'tour/partials/operation-day.html', context)

    context = {'form': OperationForm()}
    return render(request, 'tour/operation.html', context)

def create_operation_item(request, day_id):
    day = OperationDay.objects.get(id = day_id)
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        
        form = OperationItemForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.day = day
            new.save()
            
            return HttpResponse('')

    context={
        'formitem' : OperationItemForm(),
        'day' : day 
    }
    return render(request, 'tour/partials/operation-item-form.html', context)

def create_operation_item_add(request):
    context={
        'formitem' : OperationItemForm()    
    }
    return render(request, 'tour/partials/operation-item-form.html', context)

def operation_list(request):
    # Operasyonlarla ilişkili günleri ve günlerin operasyon öğelerini çeken sorgu
    operasyonlar = Operation.objects.all().order_by('-create_date').prefetch_related('operationday_set', 'operationday_set__operationitem_set')
    return render(request, 'tour/operation_list.html', {'operations': operasyonlar, 'title': 'Operasyon', 'createtitle': 'Operasyon Listesi'})


    
def delete_operation(request, operation_id):
    if request.method == "DELETE":
        operation = get_object_or_404(Operation, id=operation_id)
        operation.delete()
        return HttpResponse('')  # Boş bir yanıt döndür
    

def index(request):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company

    # Dates
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    # Queries
    today_jobs = OperationItem.objects.filter(company=sirket, day__date=today)
    tomorrow_jobs = OperationItem.objects.filter(company=sirket, day__date=tomorrow)
    week_jobs = OperationItem.objects.filter(company=sirket, day__date__range=[start_of_week, end_of_week])

    # Context
    context = {
        'today_jobs': today_jobs,
        'tomorrow_jobs': tomorrow_jobs,
        'week_jobs': week_jobs,
        'todaytitle': 'Bugünün İşleri',
        'tomorrowtitle': 'Yarının İşleri',
        'weektitle': 'Bu Haftanın İşleri',
        'title': 'İşler'
    }

    return render(request, 'tour/index.html', context)
from django.forms import inlineformset_factory



from django.forms import modelformset_factory


def update_operation(request, operation_id):
    operation = get_object_or_404(Operation, id=operation_id)
    operation_form = OperationForm(request.POST or None, instance=operation)

    if request.method == 'POST':
        if operation_form.is_valid():
            saved_operation = operation_form.save()
            
            for day in OperationDay.objects.filter(operation=saved_operation):
                day_form = OperationDayForm(request.POST, instance=day, prefix=f'day-{day.id}')
                if day_form.is_valid():
                    saved_day = day_form.save()

                    OperationItemFormset = modelformset_factory(OperationItem, form=OperationItemForm, extra=0)
                    item_formset = OperationItemFormset(
                        request.POST, 
                        queryset=OperationItem.objects.filter(day=saved_day), 
                        prefix=f'items-{saved_day.id}'
                    )

                    if item_formset.is_valid():
                        item_formset.save()
                    else:
                        # Formset hatalarını işleyin ve hata mesajlarını görüntüleyin
                        print(f"OperationItem formset errors for day {saved_day.id}: {item_formset.errors}")
                else:
                    # Day form hatalarını işleyin ve hata mesajlarını görüntüleyin
                    print(f"OperationDay form errors for day {day.id}: {day_form.errors}")
            return redirect('operation_list')
        else:
            # Operation form hatalarını işleyin ve hata mesajlarını görüntüleyin
            print(f"Operation form errors: {operation_form.errors}")

    operation_day_forms = prepare_operation_day_forms(operation)
    context = {
        'operation_form': operation_form,
        'operation_day_forms': operation_day_forms,
        'operation_id': operation_id,
    }
    return render(request, 'tour/update_operation.html', context)

def prepare_operation_day_forms(operation):
    operation_day_forms = []
    for day in OperationDay.objects.filter(operation=operation):
        day_form = OperationDayForm(instance=day, prefix=f'day-{day.id}')
        OperationItemFormset = modelformset_factory(OperationItem, form=OperationItemForm, extra=0)
        item_formset = OperationItemFormset(
            queryset=OperationItem.objects.filter(day=day), 
            prefix=f'items-{day.id}'
        )
        operation_day_forms.append((day_form, item_formset))
    return operation_day_forms


def cost_add(request):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    tour_cost = OperationItem.objects.filter(company=sirket, tour__isnull=False)
    transfer_cost = OperationItem.objects.filter(company=sirket, transfer__isnull=False)
    guide_cost = OperationItem.objects.filter(company=sirket, guide_price=1)
    hotel_cost = OperationItem.objects.filter(company=sirket, hotel_price=1)
    museum_cost = OperationItem.objects.filter(company=sirket, museym_price=1)
    activity_cost = OperationItem.objects.filter(company=sirket, activity_price=1)
    vehicle_cost = CostAddVehicleForm()
    hotel_costform = CostAddHotelForm()
    guide_costform = CostAddGuideForm()
    activity_costform = CostAddActivityForm()
    museum_costform = CostAddMuseumForm()
    context={
        'tour_cost' : tour_cost,
        'transfer_cost' : transfer_cost,
        'guide_cost' : guide_cost,
        'hotel_cost' : hotel_cost,
        'museum_cost' : museum_cost,
        'activity_cost' : activity_cost,
        'vehicle_cost' : vehicle_cost,
        'hotel_costform' : hotel_costform,
        'guide_costform' : guide_costform,
        'activity_costform' : activity_costform,
        'museum_costform' : museum_costform,
    }
    
    return render(request, 'tour/cost_add.html', context)

    