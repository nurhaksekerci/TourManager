from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.forms.models import model_to_dict
from django.http import HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            try:
                requestPersonel = Personel.objects.get(user=user)
                sirket = requestPersonel.company
                UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action="Giriş yaptı.")
            except Personel.DoesNotExist:
                pass  # veya uygun bir hata mesajı göster
            return redirect('index')
        else:
            return render(request, 'tour/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'tour/login.html')

@login_required
def logout(request):
    try:
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action="Çıkış yaptı.")
    except Personel.DoesNotExist:
        pass  # veya uygun bir hata mesajı göster
    auth_logout(request)
    return redirect('login')

@login_required
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

@login_required
def create_transfer(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = TransferForm(request.POST or None)
        if form.is_valid():
            new_transfer = form.save(commit=False)
            new_transfer.company = sirket
            new_transfer.save()
            try:
                UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Transfer kaydı yapıldı. Transfer ID: {new_transfer.id} Transfer : {new_transfer}")
            except Personel.DoesNotExist:
                pass  # veya uygun bir hata mesajı göster
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

@login_required
def delete_transfer(request, transfer_id):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "DELETE":
        transfer = get_object_or_404(Transfer, id=transfer_id)
        try:
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Transfer kaydı silindi. Transfer ID: {transfer.id} Transfer : {transfer.route}")
            transfer.delete()
            return HttpResponse('')
        except Personel.DoesNotExist:
            pass  # veya uygun bir hata mesajı göster
          # Boş bir yanıt döndür

@login_required
def edit_transfer(request, transfer_id):
    transfer = get_object_or_404(Transfer, id=transfer_id)
    old_transfer = transfer.route
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "POST":
        form = TransferForm(request.POST, instance=transfer)
        if form.is_valid():
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Transfer kaydı düzenlendi. Transfer ID: {transfer.id} Transfer : {old_transfer}>{transfer.route}")
            form.save()
            return render(request, 'tour/partials/transfer-list.html', {'form': form, 'transfer': transfer})

    else:
        form = TransferForm(instance=transfer)

    return render(request, 'tour/partials/transfer-edit-form.html', {'form': form, 'transfer': transfer})

@login_required
def cancel_transfer(request, transfer_id):
    # İlgili firma nesnesini al
    transfer = get_object_or_404(Transfer, id=transfer_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/transfer-list.html', {'transfer': transfer})

@login_required
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

@login_required
def create_tour(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = TourForm(request.POST or None)
        if form.is_valid():
            new_tour = form.save(commit=False)
            new_tour.company = sirket
            new_tour.save()
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Tur kaydı yapıldı. Tur ID: {new_tour.id} Tur : {new_tour}")
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

@login_required
def delete_tour(request, tour_id):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "DELETE":
        tour = get_object_or_404(Tour, id=tour_id)
        UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Tur kaydı silindi. Tur ID: {tour.id} Tur : {tour.route}")
        tour.delete()
        return HttpResponse('')  # Boş bir yanıt döndür

@login_required
def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    old_tour = tour.route
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "POST":
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Tur kaydı düzenlendi. Tur ID: {tour.id} Tur : {old_tour}>{tour.route}")
            return render(request, 'tour/partials/tour-list.html', {'form': form, 'tour': tour})

    else:
        form = TourForm(instance=tour)

    return render(request, 'tour/partials/tour-edit-form.html', {'form': form, 'tour': tour})

@login_required
def cancel_tour(request, tour_id):
    # İlgili firma nesnesini al
    tour = get_object_or_404(Tour, id=tour_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/tour-list.html', {'tour': tour})



@login_required
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

@login_required
def create_vehicle(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = VehicleForm(request.POST or None)
        if form.is_valid():
            new_vehicle = form.save(commit=False)
            new_vehicle.company = sirket
            new_vehicle.save()
            try:
                UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Araç kaydı yapıldı. Araç ID: {new_vehicle.id} Araç Adı: {new_vehicle.vehicle} Araç Kapasite: {new_vehicle.capacity}")
            except Personel.DoesNotExist:
                pass  # veya uygun bir hata mesajı göster

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

@login_required
def delete_vehicle(request, vehicle_id):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "DELETE":
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Araç kaydı silindi. Araç ID: {vehicle.id} Araç Adı: {vehicle.vehicle} Araç Kapasite: {vehicle.capacity}")
        vehicle.delete()
        return HttpResponse('')  # Boş bir yanıt döndür

@login_required
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    old_vehicle = vehicle.vehicle
    old_capacity = vehicle.capacity
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company

    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            action=f"Araç ID: {vehicle.id} "
            if old_vehicle != vehicle.vehicle:
                action +=f"Araç Adı : {old_vehicle}>{vehicle.vehicle} "
            else:
                action += ""
            if old_capacity != vehicle.capacity:
                action +=f"Kapasite : {old_capacity}>{vehicle.capacity} "
            else:
                action += ""

            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Araç Güncellendi. {action}")
            return render(request, 'tour/partials/vehicle-list.html', {'form': form, 'vehicle': vehicle})

    else:
        form = VehicleForm(instance=vehicle)

    return render(request, 'tour/partials/vehicle-edit-form.html', {'form': form, 'vehicle': vehicle})

@login_required
def cancel_vehicle(request, vehicle_id):
    # İlgili firma nesnesini al
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/vehicle-list.html', {'vehicle': vehicle})


@login_required
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

@login_required
def create_guide(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = GuideForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Rehber kaydı yapıldı. Rehber Id : {new.id} Rehber Adı : {new.name}")

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

@login_required
def delete_guide(request, guide_id):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "DELETE":
        guide = get_object_or_404(Guide, id=guide_id)
        UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Rehber kaydı silindi. Rehber ID : {guide.id} Rehber Adı : {guide.name}")
        guide.delete()
        return HttpResponse('')  # Boş bir yanıt döndür


@login_required
def edit_guide(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id)
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    old_name = guide.name
    old_city = guide.city
    old_document_no = guide.document_no
    old_phone = guide.phone
    old_mail = guide.mail
    old_price = guide.price
    old_currency = guide.currency
    if request.method == "POST":
        form = GuideForm(request.POST, instance=guide)
        if form.is_valid():
            # Değişiklikleri tespit etmek için eski değerleri saklayın


            # Formu kaydedin
            form.save()
            guide.refresh_from_db()
            # Değişiklikleri kontrol edin ve eylem metnini oluşturun
            action = f"Rehber kaydı düzenlendi. Rehber ID : {guide.id} "
            if old_name != guide.name:
                action += f"Ad : {old_name}>{guide.name} "
            if old_city != guide.city:
                action += f"Şehir : {old_city}>{guide.city} "
            if old_document_no != guide.document_no:
                action += f"Belge No : {old_document_no}>{guide.document_no} "
            if old_phone != guide.phone:
                action += f"Telefon : {old_phone}>{guide.phone} "
            if old_mail != guide.mail:
                action += f"Mail : {old_mail}>{guide.mail} "
            if old_price != guide.price:
                action += f"Ücret : {old_price}>{guide.price} "
            if old_currency != guide.currency:
                action += f"Para Birimi : {old_currency}>{guide.currency} "

            # Eylem kaydını oluşturun
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=action)

            return render(request, 'tour/partials/guide-list.html', {'form': form, 'guide': guide})

    else:
        form = GuideForm(instance=guide)

    return render(request, 'tour/partials/guide-edit-form.html', {'form': form, 'guide': guide})


@login_required
def cancel_guide(request, guide_id):
    # İlgili firma nesnesini al
    guide = get_object_or_404(Guide, id=guide_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/guide-list.html', {'guide': guide})


@login_required
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

@login_required
def create_hotel(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = HotelForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Otel kaydı yapıldı. Otel : {new}")
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

@login_required
def delete_hotel(request, hotel_id):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "DELETE":
        hotel = get_object_or_404(Hotel, id=hotel_id)
        UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Otel kaydı silindi. Otel : {hotel}")
        hotel.delete()
        return HttpResponse('')  # Boş bir yanıt döndür

@login_required
def edit_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    old_hotel =f"{hotel.city} {hotel.name}"
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "POST":
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Otel kaydı düzenlendi. Otel : {old_hotel}>{hotel}")
            return render(request, 'tour/partials/hotel-list.html', {'form': form, 'hotel': hotel})

    else:
        form = HotelForm(instance=hotel)

    return render(request, 'tour/partials/hotel-edit-form.html', {'form': form, 'hotel': hotel})

@login_required
def cancel_hotel(request, hotel_id):
    # İlgili firma nesnesini al
    hotel = get_object_or_404(Hotel, id=hotel_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/hotel-list.html', {'hotel': hotel})


@login_required
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

@login_required
def create_activity(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = ActivityForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Aktivite kaydı yapıldı. Aktivite : {new}")
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

@login_required
def delete_activity(request, activity_id):
    if request.method == "DELETE":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        activity = get_object_or_404(Activity, id=activity_id)
        UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Aktivite kaydı silindi. Aktivite : {activity}")
        activity.delete()
        return HttpResponse('')  # Boş bir yanıt döndür

@login_required
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    old_activity =f"{activity.city} {activity.name}"
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Aktivite kaydı düzenlendi. Aktivite : {old_activity}>{activity}")
            return render(request, 'tour/partials/activity-list.html', {'form': form, 'activity': activity})

    else:
        form = ActivityForm(instance=activity)

    return render(request, 'tour/partials/activity-edit-form.html', {'form': form, 'activity': activity})

@login_required
def cancel_activity(request, activity_id):
    # İlgili firma nesnesini al
    activity = get_object_or_404(Activity, id=activity_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/activity-list.html', {'activity': activity})


@login_required
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

@login_required
def create_personel(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = PersonelForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Personel kaydı yapıldı. Personel : {new}")
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

@login_required
def delete_personel(request, personel_id):
    if request.method == "DELETE":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        personel = get_object_or_404(Personel, id=personel_id)

        # İlişkili User modelini de sil
        if personel.user:
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Personel kaydı silindi. Personel : {personel}")

            personel.user.delete()

        personel.delete()
        return HttpResponse('')  # Boş bir yanıt döndür

@login_required
def edit_personel(request, personel_id):
    personel = get_object_or_404(Personel, id=personel_id)
    old_personel = personel.user.username
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = PersonelForm(request.POST, instance=personel)
        if form.is_valid():
            form.save()
            personel.refresh_from_db()
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Personel kaydı düzenlendi. Personel : {old_personel}>{personel}")
            return render(request, 'tour/partials/personel-list.html', {'form': form, 'personel': personel})
        else:
            print(form.errors)
    else:
        form = PersonelForm(instance=personel)

    return render(request, 'tour/partials/personel-edit-form.html', {'form': form, 'personel': personel})

@login_required
def cancel_personel(request, personel_id):
    # İlgili firma nesnesini al
    personel = get_object_or_404(Personel, id=personel_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/personel-list.html', {'personel': personel})


@login_required
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

@login_required
def create_supplier(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = SupplierForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Tedarikçi kaydı yapıldı. Tedarikçi : {new}")
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

@login_required
def delete_supplier(request, supplier_id):
    if request.method == "DELETE":
        supplier = get_object_or_404(Supplier, id=supplier_id)
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Tedarikçi kaydı silindi. Tedarikçi : {supplier}")
        supplier.delete()
        return HttpResponse('')  # Boş bir yanıt döndür

@login_required
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

@login_required
def cancel_supplier(request, supplier_id):
    # İlgili firma nesnesini al
    supplier = get_object_or_404(Supplier, id=supplier_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/supplier-list.html', {'supplier': supplier})

@login_required
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

@login_required
def create_activity_supplier(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = ActivitySupplierForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Aktivite Tedarikçi kaydı yapıldı. Aktivite TEdarikçi : {new}")
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

@login_required
def delete_activity_supplier(request, supplier_id):
    if request.method == "DELETE":
        supplier = get_object_or_404(ActivitySupplier, id=supplier_id)
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Aktivite Tedarikçi kaydı silindi. Aktivite Tedarikçi : {supplier}")
        supplier.delete()
        return HttpResponse('')  # Boş bir yanıt döndür

@login_required
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

@login_required
def cancel_activity_supplier(request, supplier_id):
    # İlgili firma nesnesini al
    supplier = get_object_or_404(ActivitySupplier, id=supplier_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/supplier-list.html', {'supplier': supplier})

@login_required
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

@login_required
def create_cost(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = CostForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Araç Maliyet kaydı yapıldı. Araç Maliyet : {new}")
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

@login_required
def delete_cost(request, cost_id):
    if request.method == "DELETE":
        cost = get_object_or_404(Cost, id=cost_id)
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Araç Maliyet kaydı silindi. Araç Maliyet : {cost}")
        cost.delete()
        return HttpResponse('')  # Boş bir yanıt döndür

@login_required
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

@login_required
def cancel_cost(request, cost_id):
    # İlgili firma nesnesini al
    cost = get_object_or_404(Cost, id=cost_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/cost-list.html', {'cost': cost})


@login_required
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
        'museums' : Museum.objects.filter(company = sirket)

    }

    return render(request, 'tour/museum.html', context)

@login_required
def create_museum(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = MuseumForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Müze kaydı yapıldı. Müze : {new}")
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

@login_required
def delete_museum(request, museum_id):
    if request.method == "DELETE":
        museum = get_object_or_404(Museum, id=museum_id)
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Müze kaydı silindi. Müze : {museum}")
        museum.delete()
        return HttpResponse('')  # Boş bir yanıt döndür

@login_required
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

@login_required
def cancel_museum(request, museum_id):
    # İlgili firma nesnesini al
    museum = get_object_or_404(Museum, id=museum_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/museum-list.html', {'museum': museum})

@login_required
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

@login_required
def create_buyer(request):
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        form = BuyerCompanyForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.company = sirket
            new.save()
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Alıcı Firma kaydı yapıldı. Alıcı Firma : {new}")
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

@login_required
def delete_buyer(request, buyer_id):
    if request.method == "DELETE":
        buyer = get_object_or_404(BuyerCompany, id=buyer_id)
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Alıcı Firma kaydı silindi. Alıcı Firma : {buyer}")
        buyer.delete()
        return HttpResponse('')  # Boş bir yanıt döndür

@login_required
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

@login_required
def cancel_buyer(request, buyer_id):
    # İlgili firma nesnesini al
    buyer = get_object_or_404(BuyerCompany, id=buyer_id)

    # Firma bilgilerini içeren bir template döndür
    return render(request, 'tour/partials/buyer-list.html', {'buyer': buyer})


@login_required
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

@login_required
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
                    try:
                        UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Operasyon kaydı yapıldı. Operasyon ID: {operasyon.id} Operasyon Etiket: {operasyon.ticket}")
                    except Personel.DoesNotExist:
                        pass  # veya uygun bir hata mesajı göster

            context = {
                'operasyon': operasyon,
                'days' : OperationDay.objects.filter(company=sirket, operation=operasyon),
                'formitem' : OperationItemForm()
            }
            return render(request, 'tour/partials/operation-day.html', context)

    context = {'form': OperationForm()}
    return render(request, 'tour/operation.html', context)

@login_required
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


            if new.vehicle_price == 0 or new.vehicle_price == 0.00 or new.vehicle_price == None:
                if new.tour:
                    cost = Cost.objects.filter(company=sirket, tour=new.tour, supplier=new.supplier).first()
                else:
                    cost = Cost.objects.filter(company=sirket, transfer=new.transfer, supplier=new.supplier).first()
                if cost:
                    new.cost = cost
                    vehicle_type = new.vehicle.vehicle
                    # Araç tipine göre maliyeti güncelle
                    if vehicle_type == "Binek":
                        new.vehicle_price = cost.car
                    elif vehicle_type == "Minivan":
                        new.vehicle_price = cost.minivan
                    elif vehicle_type == "Minibüs":
                        new.vehicle_price = cost.minibus
                    elif vehicle_type == "Midibüs":
                        new.vehicle_price = cost.midibus
                    elif vehicle_type == "Otobüs":
                        new.vehicle_price = cost.bus
            new.save()
            form.save_m2m()
            return HttpResponse('')

    context={
        'formitem' : OperationItemForm(),
        'day' : day
    }
    return render(request, 'tour/partials/operation-item-form.html', context)

@login_required
def create_operation_item_add(request):
    context={
        'formitem' : OperationItemForm()
    }
    return render(request, 'tour/partials/operation-item-form.html', context)

@login_required
def operation_list(request):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    today = datetime.today()
    # Operasyonlarla ilişkili günleri ve günlerin operasyon öğelerini çeken sorgu

    operasyonlar = Operation.objects.filter(company=sirket, finish__gte=today).order_by('-create_date').prefetch_related('operationday_set', 'operationday_set__operationitem_set')
    return render(request, 'tour/operation_list.html', {'operations': operasyonlar, 'title': 'Operasyon', 'createtitle': 'Operasyon Listesi', 'comp' : False})

from django.db.models import Prefetch

@login_required
def operation_details(request, operation_id):
    # Retrieve the operation with related objects in a single query
    operation_day_prefetch = Prefetch('operationday_set', queryset=OperationDay.objects.order_by('date').prefetch_related('operationitem_set'))
    operation_supplier = get_object_or_404(Operation, id=operation_id)
    # Operation nesnesini ilgili nesnelerle birlikte tek bir sorguda alın
    operation = Operation.objects.filter(id=operation_id).prefetch_related(operation_day_prefetch).first()
    supplier_payments = PaymentDocument.objects.filter(operation = operation_supplier)

    # Check if operation exists
    if not operation:
        # Handle the case where the operation doesn't exist, e.g., return a 404 response
        return HttpResponseNotFound('Operation not found')

    context = {
        'operation': operation,
        'supplier_payments' : supplier_payments
    }

    return render(request, 'tour/partials/operation_details.html', context)

@login_required
def operation_comp_list(request):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    today = datetime.today()
    # Operasyonlarla ilişkili günleri ve günlerin operasyon öğelerini çeken sorgu
    supplier = Supplier.objects.filter(company=sirket)
    operasyonlar = Operation.objects.filter(company=sirket, finish__lt=today).order_by('-create_date').prefetch_related('operationday_set', 'operationday_set__operationitem_set')
    return render(request, 'tour/operation_list.html', {'operations': operasyonlar, 'title': 'Operasyon', 'createtitle': 'Operasyon Listesi', 'comp' : True, 'supplier' : supplier})


@login_required
def delete_operation(request, operation_id):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "DELETE":
        operation = get_object_or_404(Operation, id=operation_id)
        try:
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Operasyon kaydı silindi. Operasyon ID: {operation.id} Operasyon Etiket: {operation.ticket}")
        except Personel.DoesNotExist:
            pass  # veya uygun bir hata mesajı göster
        operation.delete()
        return HttpResponse('')  # Boş bir yanıt döndür

@login_required
def delete_operationitem(request, operationitem_id):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "DELETE":
        operationitem = get_object_or_404(OperationItem, id=operationitem_id)
        try:
            UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=f"Operasyon İtem kaydı silindi. Operasyon İtem ID: {operationitem.id} Operasyon Gün: {operationitem.day.date} Operasyon Etiket: {operationitem.day.operation.ticket}")
        except Personel.DoesNotExist:
            pass  # veya uygun bir hata mesajı göster
        operationitem.delete()
        return HttpResponse('')  # Boş bir yanıt döndür

@login_required
def index(request):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "POST":
        date = request.POST.get('date_job')
        week_jobs = OperationItem.objects.filter(company=sirket, day__date=date)
        date_parts = date.split('-')

        # Listenin sırasını tersine çevir
        reversed_date_parts = date_parts[::-1]

        # Ters çevrilmiş listeyi yazdır
        reversed_date = '.'.join(reversed_date_parts)
        weektitle = f"{reversed_date} Tarihli İşler"


    else:
        week_jobs = None
        weektitle = "Tarih Giriniz"
    # Dates
    today = datetime.today()
    tomorrow = today + timedelta(days=1)

    # Queries
    today_jobs = OperationItem.objects.filter(company=sirket, day__date=today).order_by('pick_time')
    tomorrow_jobs = OperationItem.objects.filter(company=sirket, day__date=tomorrow).order_by('pick_time')
    # Python'da sıralama yapın

    # Context
    context = {
        'today_jobs': today_jobs,
        'tomorrow_jobs': tomorrow_jobs,
        'week_jobs': week_jobs,
        'todaytitle': today,
        'tomorrowtitle': tomorrow,
        'weektitle': weektitle,
        'title': 'İşler'
    }

    return render(request, 'tour/index.html', context)

@login_required
def indexim(request):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "POST":
        date = request.POST.get('date_job')
        week_jobs = OperationItem.objects.filter(company=sirket, day__date=date, day__operation__follow_staff=requestPersonel)
        date_parts = date.split('-')

        # Listenin sırasını tersine çevir
        reversed_date_parts = date_parts[::-1]

        # Ters çevrilmiş listeyi yazdır
        reversed_date = '.'.join(reversed_date_parts)
        weektitle = f"{reversed_date} Tarihli İşler"


    else:
        week_jobs = None
        weektitle = "Tarih Giriniz"
    # Dates
    today = datetime.today()
    tomorrow = today + timedelta(days=1)

    # Queries
    today_jobs = OperationItem.objects.filter(company=sirket, day__date=today, day__operation__follow_staff=requestPersonel).order_by('pick_time')
    tomorrow_jobs = OperationItem.objects.filter(company=sirket, day__date=tomorrow, day__operation__follow_staff=requestPersonel).order_by('pick_time')
    # Python'da sıralama yapın

    # Context
    context = {
        'today_jobs': today_jobs,
        'tomorrow_jobs': tomorrow_jobs,
        'week_jobs': week_jobs,
        'todaytitle': today,
        'tomorrowtitle': tomorrow,
        'weektitle': weektitle,
        'title': 'İşler'
    }

    return render(request, 'tour/index.html', context)
from django.forms import inlineformset_factory
from django.forms import modelformset_factory




@login_required
def cost_add(request):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)
    guide_cost = OperationItem.objects.filter(company=sirket, guide_price=1, guide__isnull=True, day__date__in=[today, tomorrow, day_after_tomorrow]).order_by('day__date')
    hotel_cost = OperationItem.objects.filter(company=sirket, hotel_price=1, hotel__isnull=True, day__date__in=[today, tomorrow, day_after_tomorrow]).order_by('day__date')
    museum_cost = OperationItem.objects.filter(company=sirket, museym_price=1, day__date__in=[today, tomorrow, day_after_tomorrow]).order_by('day__date')
    activity_cost = OperationItem.objects.filter(company=sirket, activity_price=1, day__date__in=[today, tomorrow, day_after_tomorrow]).order_by('day__date')
    day_after_tomorrow = today + timedelta(days=2)
    tour_cost = OperationItem.objects.filter(day__date__in=[today, tomorrow, day_after_tomorrow], company=sirket, tour__isnull=False, supplier__isnull=True).order_by('day__date')
    transfer_cost = OperationItem.objects.filter(day__date__in=[today, tomorrow, day_after_tomorrow], company=sirket, transfer__isnull=False, supplier__isnull=True).order_by('day__date')
    driver_cost = OperationItem.objects.filter(day__date__in=[today, tomorrow, day_after_tomorrow], company=sirket, cost__isnull=False, plaka__isnull=True).order_by('day__date')
    vehicle_cost = CostAddVehicleForm()
    driver_form = DriverForm()
    hotel_costform = CostAddHotelForm()
    guide_costform = CostAddGuideForm()
    activity_costform = CostAddActivityForm()
    museum_costform = CostAddMuseumForm()

    context={
        'title' : 'Tedarikçi Atama',
        'guide_cost' : guide_cost,
        'hotel_cost' : hotel_cost,
        'museum_cost' : museum_cost,
        'activity_cost' : activity_cost,
        'hotel_costform' : hotel_costform,
        'guide_costform' : guide_costform,
        'activity_costform' : activity_costform,
        'museum_costform' : museum_costform,
        'title' : 'Tedarikçi Atama',
        'tour_cost' : tour_cost,
        'transfer_cost' : transfer_cost,
        'vehicle_cost' : vehicle_cost,
        'driver_cost' : driver_cost,
        'driver_form' : driver_form,

    }

    return render(request, 'tour/cost_add.html', context)

@login_required
def cost_add_vehicle(request):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)
    tour_cost = OperationItem.objects.filter(day__date__in=[today, tomorrow, day_after_tomorrow], company=sirket, tour__isnull=False, cost__isnull=True).order_by('day__date')
    transfer_cost = OperationItem.objects.filter(day__date__in=[today, tomorrow, day_after_tomorrow], company=sirket, transfer__isnull=False, cost__isnull=True).order_by('day__date')
    driver_cost = OperationItem.objects.filter(day__date__in=[today, tomorrow, day_after_tomorrow], company=sirket, supplier__isnull=False, plaka__isnull=True).order_by('day__date')
    vehicle_cost = CostAddVehicleForm()
    driver_form = DriverForm()


    context={
        'title' : 'Tedarikçi Atama',
        'tour_cost' : tour_cost,
        'transfer_cost' : transfer_cost,
        'vehicle_cost' : vehicle_cost,
        'driver_cost' : driver_cost,
        'driver_form' : driver_form,
    }

    return render(request, 'tour/cost_add.html', context)
from django.db.models import Count, Min, Max

@login_required
def update_operation(request, operation_id):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    operation = get_object_or_404(Operation, id=operation_id)
    old_follow_staff = operation.follow_staff
    old_buyer_company = operation.buyer_company
    old_start = operation.start
    old_finish = operation.finish
    old_passenger_info = operation.passenger_info
    old_ticket = operation.ticket
    old_usd_sales_price = operation.usd_sales_price
    old_tl_sales_price = operation.tl_sales_price
    old_eur_sales_price = operation.eur_sales_price
    old_rbm_sales_price = operation.rbm_sales_price
    old_number_passengers = operation.number_passengers
    old_payment_type = operation.payment_type
    old_payment_channel = operation.payment_channel
    if request.method == "POST":
        form = OperationForm(request.POST, instance=operation)
        if form.is_valid():
            form.save()
            operation.refresh_from_db()
            # Bitiş tarihi değişikliğini kontrol et
            # Yeni bitiş tarihi eski bitiş tarihinden büyükse yeni günler oluştur
            # Yeni günler eklemek
            if operation.finish > old_finish:
                current_date = old_finish + timedelta(days=1)
                while current_date <= operation.finish:
                    operasyon_gun, created = OperationDay.objects.get_or_create(
                        date=current_date,
                        operation=operation,
                        defaults={'company': sirket}
                    )
                    if created:
                        print(f"Yeni operasyon günü oluşturuldu: {operasyon_gun.date}")
                    current_date += timedelta(days=1)

            # Günleri silerken ilişkili operation item kontrolü
            days_with_items = OperationDay.objects.filter(operation=operation).annotate(items_count=Count('operationitem')).filter(items_count__gt=0)

            if operation.finish < old_finish:
                # İlişkili item'ları olan günleri koru ve operation.finish'i güncelle
                max_date = days_with_items.filter(date__gt=operation.finish).aggregate(max_date=Max('date'))['max_date']
                if max_date:
                    operation.finish = max_date
                    operation.save()

                # İlişkisi olmayan günleri sil
                OperationDay.objects.filter(operation=operation, date__gt=operation.finish).exclude(id__in=days_with_items.values('id')).delete()

            if operation.start > old_start:
                # İlişkili item'ları olan günleri koru ve operation.start'ı güncelle
                min_date = days_with_items.filter(date__lt=operation.start).aggregate(min_date=Min('date'))['min_date']
                if min_date:
                    operation.start = min_date
                    operation.save()

                # İlişkisi olmayan günleri sil
                OperationDay.objects.filter(operation=operation, date__lt=operation.start).exclude(id__in=days_with_items.values('id')).delete()

            # Yeni başlangıç tarihi eski başlangıç tarihinden küçükse, aradaki yeni günler için OperationDay nesneleri oluştur
            if operation.start < old_start:
                current_date = operation.start
                while current_date < old_start:
                    operasyon_gun, created = OperationDay.objects.get_or_create(
                        date=current_date,
                        operation=operation,
                        defaults={'company': sirket}
                    )
                    if created:
                        print(f"Yeni operasyon günü oluşturuldu: {operasyon_gun.date}")
                    current_date += timedelta(days=1)


            action = ""
            if any([
                old_follow_staff != operation.follow_staff,
                old_buyer_company != operation.buyer_company,
                old_start != operation.start,
                old_finish != operation.finish,
                old_passenger_info != operation.passenger_info,
                old_ticket != operation.ticket,
                old_usd_sales_price != operation.usd_sales_price,
                old_tl_sales_price != operation.tl_sales_price,
                old_eur_sales_price != operation.eur_sales_price,
                old_rbm_sales_price != operation.rbm_sales_price,
                old_number_passengers != operation.number_passengers,
                old_payment_channel != operation.payment_channel,
                old_payment_type != operation.payment_type
            ]):
                action = f"Operasyon Güncellendi. Operasyon ID : {operation.id}"
                # Diğer değişiklikleri kontrol eden if blokları
                if old_follow_staff != operation.follow_staff:
                    action += f" Takip Eden Personel: {old_follow_staff}>{operation.follow_staff}"
                if old_buyer_company != operation.buyer_company:
                    action += f" Alıcı Şirket: {old_buyer_company}>{operation.buyer_company}"
                if old_start != operation.start:
                    action += f" Başlangıç Tarihi: {old_start}>{operation.start}"
                if old_finish != operation.finish:
                    action += f" Bitiş Tarihi: {old_finish}>{operation.finish}"
                if old_passenger_info != operation.passenger_info:
                    action += f" Yolcu Bilgisi: {old_passenger_info}>{operation.passenger_info}"
                if old_ticket != operation.ticket:
                    action += f" Etiket : {old_ticket}>{operation.ticket}"
                if old_usd_sales_price != operation.usd_sales_price:
                    action += f" USD Satış Fiyatı: {old_usd_sales_price}>{operation.usd_sales_price}"
                if old_tl_sales_price != operation.tl_sales_price:
                    action += f" TL Satış Fiyatı: {old_tl_sales_price}>{operation.tl_sales_price}"
                if old_eur_sales_price != operation.eur_sales_price:
                    action += f" EUR Satış Fiyatı: {old_eur_sales_price}>{operation.eur_sales_price}"
                if old_rbm_sales_price != operation.rbm_sales_price:
                    action += f" RBM Satış Fiyatı: {old_rbm_sales_price}>{operation.rbm_sales_price}"
                if old_number_passengers != operation.number_passengers:
                    action += f" Yolcu Sayısı: {old_number_passengers}>{operation.number_passengers}"
                if old_payment_type != operation.payment_type:
                    action += f" Ödeme Türü: {old_payment_type}>{operation.payment_type}"
                if old_payment_channel != operation.payment_channel:
                    action += f" Ödeme Kanalı: {old_payment_channel}>{operation.payment_channel}"

            if action:  # Eğer action doluysa, log kaydını oluştur
                try:
                    UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=action)
                except Personel.DoesNotExist:
                    pass  # veya uygun bir hata mesajı göster


            # İşlem başarılı olduğunda bir mesaj göster
            messages.success(request, "Operasyon başarıyla güncellendi.")
            return redirect('operation_details', operation_id=operation.id)

    else:
        form = OperationForm(instance=operation)

    # Operasyon günleri ve ilgili öğeler için form setleri hazırla
    operation_day_forms = [
        (OperationDayForm(instance=day), [OperationItemForm(instance=item) for item in day.operationitem_set.all()])
        for day in operation.operationday_set.all().order_by('date')
    ]


    return render(request, 'tour/update_operation.html', {'operation_form': form, 'title': 'Güncelle', 'operation_day_forms': operation_day_forms})
import random

@login_required
def update_or_add_operation_item(request, day_id, item_id=None):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    operation_day = get_object_or_404(OperationDay, id=day_id)
    url = "http://soap.netgsm.com.tr:8080/Sms_webservis/SMS?wsdl"
    headers = {'content-type': 'text/xml'}
    operation_item = None if item_id is None else get_object_or_404(OperationItem, id=item_id)
    if operation_item:
        if operation_item.guide:
            old_guide = operation_item.guide.name
            old_guide_phone = operation_item.guide.phone
        else:
            old_guide = None
            old_guide_phone = None
        if operation_item.driver:
            old_driver = operation_item.driver
            old_driver_phone = operation_item.driver_phone
        else:
            old_driver = None
            old_driver_phone = None
    if request.method == "POST":
        if operation_item is not None:
            old_operation_type = operation_item.operation_type
            old_pick_time = operation_item.pick_time
            old_description = operation_item.description
            old_tour = operation_item.tour
            old_transfer = operation_item.transfer
            old_vehicle = operation_item.vehicle
            old_activity = operation_item.activity
            old_museum = operation_item.museum
            old_hotel = operation_item.hotel
            old_room_type = operation_item.room_type
            old_hotel_price = operation_item.hotel_price
            old_hotel_currency = operation_item.hotel_currency
            old_guide_price = operation_item.guide_price
            old_guide_currency = operation_item.guide_currency
            old_activity_price = operation_item.activity_price
            old_activity_currency = operation_item.activity_currency
            old_museym_price = operation_item.museym_price
            old_museum_currency = operation_item.museum_currency
            old_other_price = operation_item.other_price
            old_other_currency = operation_item.other_currency
            old_activity_cost = operation_item.activity_cost
            old_cost = operation_item.cost
            old_plaka = operation_item.plaka
            old_supplier = operation_item.supplier
            old_vehicle_price = operation_item.vehicle_price
        else:
            old_operation_type = None
            old_pick_time = None
            old_description = None
            old_tour = None
            old_transfer = None
            old_vehicle = None
            old_guide = None
            old_activity = None
            old_museum = None
            old_hotel = None
            old_room_type = None
            old_hotel_price = None
            old_hotel_currency = None
            old_guide_price = None
            old_guide_currency = None
            old_activity_price = None
            old_activity_currency = None
            old_museym_price = None
            old_museum_currency = None
            old_other_price = None
            old_other_currency = None
            old_activity_cost = None
            old_cost = None
            old_driver = None
            old_driver_phone = None
            old_plaka = None
            old_supplier = None
            old_vehicle_price = None

        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        formitem = OperationItemForm(request.POST, instance=operation_item)
        if formitem.is_valid():
            operation_item = formitem.save(commit=False)
            operation_item.day = operation_day
            operation_item.company = sirket
            operation_item.save()
            operation_item.refresh_from_db()
            action = ""
            #############################################################################

            if operation_item.cost == None or operation_item.supplier != old_supplier:
                if operation_item.tour:
                    cost = Cost.objects.filter(company=sirket, tour=operation_item.tour, supplier=operation_item.supplier).first()
                else:
                    cost = Cost.objects.filter(company=sirket, transfer=operation_item.transfer, supplier=operation_item.supplier).first()
                if cost:
                    operation_item.cost = cost
                    vehicle_type = operation_item.vehicle.vehicle
                    # Araç tipine göre maliyeti güncelle
                    if vehicle_type == "Binek":
                        operation_item.vehicle_price = cost.car
                    elif vehicle_type == "Minivan":
                        operation_item.vehicle_price = cost.minivan
                    elif vehicle_type == "Minibüs":
                        operation_item.vehicle_price = cost.minibus
                    elif vehicle_type == "Midibüs":
                        operation_item.vehicle_price = cost.midibus
                    elif vehicle_type == "Otobüs":
                        operation_item.vehicle_price = cost.bus
                    # Değişiklikleri kaydet
            operation_item.save()
            formitem.save_m2m()
                    # Log mesajı oluştur
            action = f"Yeni tedarikçi atandı ve maliyet güncellendi. Tedarikçi: {operation_item.supplier}, Maliyet: {operation_item.vehicle_price} ₺"
            try:
                UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=action)
            except Personel.DoesNotExist:
                pass  # veya uygun bir hata mesajı göster
            #############################################################################
            if any([
                old_operation_type != operation_item.operation_type,
                old_pick_time != operation_item.pick_time,
                old_description != operation_item.description,
                old_tour != operation_item.tour,
                old_transfer != operation_item.transfer,
                old_vehicle != operation_item.vehicle,
                old_guide != operation_item.guide,
                old_activity != operation_item.activity,
                old_museum != operation_item.museum,
                old_hotel != operation_item.hotel,
                old_room_type != operation_item.room_type,
                old_hotel_price != operation_item.hotel_price,
                old_hotel_currency != operation_item.hotel_currency,
                old_guide_price != operation_item.guide_price,
                old_guide_currency != operation_item.guide_currency,
                old_activity_price != operation_item.activity_price,
                old_activity_currency != operation_item.activity_currency,
                old_museym_price != operation_item.museym_price,
                old_museum_currency != operation_item.museum_currency,
                old_other_price != operation_item.other_price,
                old_other_currency != operation_item.other_currency,
                old_activity_cost != operation_item.activity_cost,
                old_cost != operation_item.cost,
                old_driver != operation_item.driver,
                old_driver_phone != operation_item.driver_phone,
                old_plaka != operation_item.plaka,
                old_supplier != operation_item.supplier,
                old_vehicle_price != operation_item.vehicle_price
            ]):
                action = f"Operasyon İtem Kaydı Güncellendi. Operasyon İtem ID : {operation_item.id} "


            if old_operation_type != operation_item.operation_type:
                action += f"İşlem Türü : {old_operation_type}>{operation_item.operation_type} "
            if old_pick_time != operation_item.pick_time:
                action += f"Alış Saati : {old_pick_time}>{operation_item.pick_time} "
            if old_description != operation_item.description:
                action += f"Açıklama : {old_description}>{operation_item.description} "
            if old_tour != operation_item.tour:
                action += f"Tur : {old_tour}>{operation_item.tour} "
            if old_transfer != operation_item.transfer:
                action += f"Transfer : {old_transfer}>{operation_item.transfer} "
            if old_vehicle != operation_item.vehicle:
                action += f"Araç : {old_vehicle}>{operation_item.vehicle} "
            # Rehber değişikliğini doğru bir şekilde kontrol et
            if old_guide != operation_item.guide:
                action += f"Rehber : {old_guide}>{operation_item.guide} "
            if old_activity != operation_item.activity:
                action += f"Aktivite : {old_activity}>{operation_item.activity} "
            if old_museum != operation_item.museum:
                action += f"Müze : {old_museum}>{operation_item.museum} "
            if old_hotel != operation_item.hotel:
                action += f"Otel : {old_hotel}>{operation_item.hotel} "
            if old_room_type != operation_item.room_type:
                action += f"Oda : {old_room_type}>{operation_item.room_type} "
            if old_hotel_price != operation_item.hotel_price:
                action += f"Otel Ücreti : {old_hotel_price}>{operation_item.hotel_price} "
            if old_hotel_currency != operation_item.hotel_currency:
                action += f"Otel PAra Birimi : {old_hotel_currency}>{operation_item.hotel_currency} "
            if old_guide_price != operation_item.guide_price:
                action += f"Rehber Ücreti : {old_guide_price}>{operation_item.guide_price} "
            if old_guide_currency != operation_item.guide_currency:
                action += f"Rehber PAra Birimi : {old_guide_currency}>{operation_item.guide_currency} "
            if old_activity_price != operation_item.activity_price:
                action += f"Aktivite Ücreti : {old_activity_price}>{operation_item.activity_price} "
            if old_activity_currency != operation_item.activity_currency:
                action += f"Aktivite Para Birimi : {old_activity_currency}>{operation_item.activity_currency} "
            if old_museym_price != operation_item.museym_price:
                action += f"Müze Ücreti : {old_museym_price}>{operation_item.museym_price} "
            if old_museum_currency != operation_item.museum_currency:
                action += f"Müze Para Birimi : {old_museum_currency}>{operation_item.museum_currency} "
            if old_other_price != operation_item.other_price:
                action += f"Diğer Ücretler : {old_other_price}>{operation_item.other_price} "
            if old_other_currency != operation_item.other_currency:
                action += f"Diğer Para Birimi : {old_other_currency}>{operation_item.other_currency} "
            if old_activity_cost != operation_item.activity_cost:
                action += f"Aktivite Maliyeti : {old_activity_cost}>{operation_item.activity_cost} "
            if old_cost != operation_item.cost:
                action += f"Toplam Maliyet : {old_cost}>{operation_item.cost} "
            if old_driver != operation_item.driver:
                action += f"Sürücü : {old_driver}>{operation_item.driver} "
            if old_driver_phone != operation_item.driver_phone:
                action += f"Sürücü Telefonu : {old_driver_phone}>{operation_item.driver_phone} "
            if old_plaka != operation_item.plaka:
                action += f"Plaka : {old_plaka}>{operation_item.plaka} "
            if old_supplier != operation_item.supplier:
                action += f"Tedarikçi : {old_supplier}>{operation_item.supplier} "
            if old_vehicle_price != operation_item.vehicle_price:
                action += f"Araç Ücreti : {old_vehicle_price}>{operation_item.vehicle_price} "
            if action:  # Eğer action doluysa, log kaydını oluştur
                try:
                    UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=action)
                except Personel.DoesNotExist:
                    pass  # veya uygun bir hata mesajı göster
        return HttpResponse('')
    else:
        formitem = OperationItemForm()

    return render(request, 'tour/partials/update_formitem_add.html', {'formitem': formitem, 'day_id': day_id, 'random_number': random.randint(1000, 9999)})

@login_required
def vehicle_cost_add(request, item_id):
    operation_item = get_object_or_404(OperationItem, id=item_id)
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "POST":
        formitem = CostAddVehicleForm(request.POST, instance=operation_item)
        if formitem.is_valid():

            # Burada başarılı kayıt için bir mesaj eklenebilir
            supplier_form = formitem.cleaned_data['supplier']
            price_form = formitem.cleaned_data['vehicle_price']
            cost = None
            if operation_item.tour is None:
                cost = Cost.objects.filter(company=sirket, transfer=operation_item.transfer, supplier=supplier_form).first()
            else:
                cost = Cost.objects.filter(company=sirket, tour=operation_item.tour, supplier=supplier_form).first()
            action = f"Operasyon İtem Kaydına Tedarikçi Eklendi. Operasyon İtem ID : {operation_item.id} "
            if cost:
                operation_item.cost = cost
                if price_form == 0:
                    vehicle_type = operation_item.vehicle.vehicle
                    if vehicle_type == "Binek":
                        operation_item.vehicle_price = cost.car
                        action += "Araç : Binek "
                    elif vehicle_type == "Minivan":
                        operation_item.vehicle_price = cost.minivan
                        action += "Araç : Minivan "
                    elif vehicle_type == "Minibüs":
                        operation_item.vehicle_price = cost.minibus
                        action += "Araç : Minibüs "
                    elif vehicle_type == "Midibüs":
                        operation_item.vehicle_price = cost.midibus
                        action += "Araç : Midibüs "
                    elif vehicle_type == "Otobüs":
                        operation_item.vehicle_price = cost.bus
                        action += "Araç : Otobüs "
                operation_item.save()
                formitem.save()
                operation_item.refresh_from_db()
                action += f"Tedarikçi : {operation_item.supplier} "
                action += f"Maliyet : {operation_item.vehicle_price} ₺"

                try:
                    UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=action)
                except Personel.DoesNotExist:
                    pass  # veya uygun bir hata mesajı göster
            else:
                # cost bulunamadı, uygun bir hata mesajı döndürün veya işlemi durdurun
                return HttpResponse('Cost bulunamadı.', status=400)

            return HttpResponse('Form başarıyla kaydedildi.')
        else:
            # Form geçersizse bir hata mesajı döndür
            return HttpResponse('Form geçersiz.', status=400)
    return HttpResponse('')  # GET isteği için boş yanıt

import requests
import html

@login_required
def drive_cost_add(request, item_id):
    operation_item = get_object_or_404(OperationItem, id=item_id)
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    if request.method == "POST":
        formitem = DriverForm(request.POST, instance=operation_item)
        if formitem.is_valid():
            formitem.save()
            driver_phone = operation_item.driver_phone  # Doğru veriye erişim
            driver = operation_item.driver
            url = "http://soap.netgsm.com.tr:8080/Sms_webservis/SMS?wsdl"
            headers = {'content-type': 'text/xml'}
            tarih= operation_item.day.date
            op_type = operation_item.operation_type
            desc = operation_item.description
            pick = operation_item.pick_time
            hotel = operation_item.hotel
            action =f"Operasyon İtem Kaydına Şoför Eklendi. Operasyon İtem ID : {operation_item.id}. Şoför : {driver}, Telefon : {driver_phone}, Plaka : {operation_item.plaka} "
            try:
                UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=action)
            except Personel.DoesNotExist:
                pass  # veya uygun bir hata mesajı göster
            if operation_item.tour == None:
                tur = ""
            else:
                tur = operation_item.tour
            if operation_item.transfer == None:
                transfer = ""
            else:
                transfer = operation_item.transfer
            mesaj = f"Sayın {driver}, {tarih} tarihinde {op_type} tanımlanmıştır. Açıklaması: {desc}, {tur}{transfer} Alış Saati: {pick}, Otel: {hotel}."
            body = f"""<?xml version="1.0"?>
                <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                         xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <SOAP-ENV:Body>
                        <ns3:smsGonder1NV2 xmlns:ns3="http://sms/">
                            <username>8503081334</username>
                            <password>6D18AD8</password>
                            <header>MNC GROUP</header>
                            <msg>{mesaj}</msg>
                            <gsm>{driver_phone}</gsm>
                            <encoding>TR</encoding>
                            <filter>0</filter>
                            <startdate></startdate>
                            <stopdate></stopdate>
                        </ns3:smsGonder1NV2>
                    </SOAP-ENV:Body>
                </SOAP-ENV:Envelope>"""

            response = requests.post(url, data=body, headers=headers)
            print(response)

            if operation_item.guide != None:
                guide = operation_item.guide.name
                guide_phone = operation_item.guide.phone
                mesaj = f"Sayın {guide}, {tarih} tarihinde {op_type} tanımlanmıştır. Açıklaması: {desc}, {tur}{transfer}  Alış Saati: {pick}, Otel: {hotel}. Şoför bilgiler: {driver} {driver_phone}"
                body = f"""<?xml version="1.0"?>
                    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                             xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <SOAP-ENV:Body>
                            <ns3:smsGonder1NV2 xmlns:ns3="http://sms/">
                                <username>8503081334</username>
                                <password>6D18AD8</password>
                                <header>MNC GROUP</header>
                                <msg>{mesaj}</msg>
                                <gsm>{guide_phone}</gsm>
                                <encoding>TR</encoding>
                                <filter>0</filter>
                                <startdate></startdate>
                                <stopdate></stopdate>
                            </ns3:smsGonder1NV2>
                        </SOAP-ENV:Body>
                    </SOAP-ENV:Envelope>"""

                response = requests.post(url, data=body, headers=headers)
                print(response)



            return HttpResponse('Form başarıyla kaydedildi.')
        else:
            return HttpResponse('Form geçersiz.', status=400)
    return HttpResponse('')  # GET isteği için boş yanıt

@login_required
def hotel_cost_add(request, item_id):
    operation_item = get_object_or_404(OperationItem, id=item_id)  # day_id yerine item_id kullanılıyor
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        formitem = CostAddHotelForm(request.POST, instance=operation_item)
        if formitem.is_valid():
            formitem.save()
            operation_item.refresh_from_db()
            action =f"Operasyon İtem Kaydına Otel Eklendi. Operasyon İtem ID : {operation_item.id}. Otel : {operation_item.hotel}, Oda : {operation_item.room_type}, Ücreti : {operation_item.hotel_price} {operation_item.hotel_currency} "
            try:
                UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=action)
            except Personel.DoesNotExist:
                pass  # veya uygun bir hata mesajı göster
            # Burada başarılı kayıt için bir mesaj eklenebilir
            return HttpResponse('Form başarıyla kaydedildi.')
        else:
            # Form geçersizse bir hata mesajı döndür
            return HttpResponse('Form geçersiz.', status=400)
    return HttpResponse('')  # GET isteği için boş yanıt

@login_required
def guide_cost_add(request, item_id):
    operation_item = get_object_or_404(OperationItem, id=item_id)  # day_id yerine item_id kullanılıyor
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        formitem = CostAddGuideForm(request.POST, instance=operation_item)
        if formitem.is_valid():
            formitem.save()
            operation_item.refresh_from_db()
            action =f"Operasyon İtem Kaydına Rehber Eklendi. Operasyon İtem ID : {operation_item.id}. Rehber : {operation_item.guide.name}, Telefon : {operation_item.guide.phone}, Ücreti : {operation_item.guide_price} {operation_item.guide_currency} "
            try:
                UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=action)
            except Personel.DoesNotExist:
                pass  # veya uygun bir hata mesajı göster
            # Burada başarılı kayıt için bir mesaj eklenebilir
            return HttpResponse('Form başarıyla kaydedildi.')
        else:
            # Form geçersizse bir hata mesajı döndür
            return HttpResponse('Form geçersiz.', status=400)
    return HttpResponse('')  # GET isteği için boş yanıt

@login_required
def activity_cost_add(request, item_id):
    operation_item = get_object_or_404(OperationItem, id=item_id)  # day_id yerine item_id kullanılıyor
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        formitem = CostAddActivityForm(request.POST, instance=operation_item)
        if formitem.is_valid():
            formitem.save()
            operation_item.refresh_from_db()
            action =f"Operasyon İtem Kaydına Aktivite Tedarikçisi Eklendi. Operasyon İtem ID : {operation_item.id}. Rehber : {operation_item.activity_cost.name}, İletişim : {operation_item.activity_cost.contact}, Ücreti : {operation_item.activity_price} {operation_item.activity_currency} "
            try:
                UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=action)
            except Personel.DoesNotExist:
                pass  # veya uygun bir hata mesajı göster
            # Burada başarılı kayıt için bir mesaj eklenebilir
            return HttpResponse('Form başarıyla kaydedildi.')
        else:
            # Form geçersizse bir hata mesajı döndür
            return HttpResponse('Form geçersiz.', status=400)
    return HttpResponse('')  # GET isteği için boş yanıt

@login_required
def museum_cost_add(request, item_id):
    operation_item = get_object_or_404(OperationItem, id=item_id)  # day_id yerine item_id kullanılıyor
    if request.method == "POST":
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        formitem = CostAddMuseumForm(request.POST, instance=operation_item)
        if formitem.is_valid():
            formitem.save()
            operation_item.refresh_from_db()
            action =f"Operasyon İtem Kaydına Müze Eklendi. Operasyon İtem ID : {operation_item.id}. Müze : {operation_item.museum.name}, İletişim : {operation_item.museum.contact}, Ücreti : {operation_item.museym_price} {operation_item.museum_currency} "
            try:
                UserActivityLog.objects.create(staff=requestPersonel, company=sirket, action=action)
            except Personel.DoesNotExist:
                pass  # veya uygun bir hata mesajı göster
            # Burada başarılı kayıt için bir mesaj eklenebilir
            return HttpResponse('Form başarıyla kaydedildi.')
        else:
            # Form geçersizse bir hata mesajı döndür
            return HttpResponse('Form geçersiz.', status=400)
    return HttpResponse('')  # GET isteği için boş yanıt

@login_required
def fiyatlandirma_islem(request, fiyat_id):
    user = request.user
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    fiyat = get_object_or_404(Fiyatlandırma, sirket=sirket, id=fiyat_id)
    if request.method == 'POST':
        onay = request.POST['onay']
        aciklama = request.POST['aciklama']
        if onay == "True":
            fiyat.islem=True
            fiyat.onay = True
            fiyat.aciklama = "Tebrikler Fiyat Onaylandı."
            fiyat.save()
        elif onay == "False":
            fiyat.islem=True
            if aciklama:
                fiyat.aciklama = aciklama
                fiyat.onay = False
                fiyat.save()
            else:
                fiyat.aciklama = "Fiyat uygun değil."
                fiyat.onay = False
                fiyat.save()
        return redirect('index')

def parse_custom_date(date):
        # Eğer date zaten datetime.date nesnesiyse, doğrudan döndür
        return date


@login_required
def create_fiyatlandirma(request):
    if request.method == 'POST':
        form = FiyatlandirmaForm(request.POST)
        formset = FiyatlandirmaItemFormSet(request.POST)
        user = request.user
        requestPersonel = Personel.objects.get(user=request.user)
        sirket = requestPersonel.company
        if form.is_valid() and formset.is_valid():
            personel = Personel.objects.get(user=user)  # User'ı Personel nesnesine dönüştür
            fiyatlandirma = form.save(commit=False)
            print("Fiyatlandirma nesnesi oluşturuldu:", fiyatlandirma)
            fiyatlandirma.olusturan = requestPersonel
            fiyatlandirma.sirket = sirket
            fiyatlandirma.save()  # Ana modeli kaydet
            print("Fiyatlandirma nesnesi kaydedildi.")
            formset.instance = fiyatlandirma  # İlişkiyi kur
            for form in formset:
                tarih_str = form.cleaned_data.get('tarih')
                tarih_obj = parse_custom_date(tarih_str)
                if tarih_obj:
                    form.cleaned_data['tarih'] = tarih_obj
                else:
                    print("Geçersiz tarih formatı:", tarih_str)
            formset.save()
            print("FiyatlandirmaItem nesneleri kaydedildi.")# İlişkili modeli kaydet
            return redirect('fiyatlandırma_list')
        else:
            print("Form geçerli değil:", form.errors)
            print("Formset geçerli değil:", formset.errors)
            # İşlem başarılıysa, başka bir sayfaya yönlendir
            return redirect('fiyatlandirma')
    else:
        form = FiyatlandirmaForm()
        formset = FiyatlandirmaItemFormSet()

    return render(request, 'fiyatlandirma.html', {'form': form, 'formset': formset, 'title': 'Fiyatlandır'})

@login_required
def fiyatlandırma_list(request):
    user = request.user
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    fiyatlandirmalar = Fiyatlandırma.objects.filter(sirket = sirket)  # Tüm personelleri alın
    return render(request, 'fiyatlandirma_list.html', {'fiyatlandirmalar': fiyatlandirmalar, 'title': 'Fiyatlandırma Listesi'})

@login_required
def fiyatlandirma_detay(request, fiyatlandirma_id):
    # Satışları alın ve ilgili satış itemlerini "prefetch_related" ile alın
    fiyatlandirma = Fiyatlandırma.objects.prefetch_related('fiyatlandirmaitem_set').get(id = fiyatlandirma_id)  # Satis modelini kendi projenizdeki modele uygun bir şekilde kullanın
    return render(request, 'fiyatlandirma_detay.html', {'fiyatlandirma': fiyatlandirma, 'title': 'Fiyatlandırma Detay'})

@login_required
def edit_fiyatlandirma(request, fiyatlandirma_id):
    fiyatlandirma = get_object_or_404(Fiyatlandırma, id=fiyatlandirma_id)

    if request.method == 'POST':
        form = FiyatlandirmaForm(request.POST, instance=fiyatlandirma)
        formset = FiyatlandirmaItemFormSet(request.POST, instance=fiyatlandirma)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('fiyatlandirma_detay', fiyatlandirma_id=fiyatlandirma_id)
        else:
            # Hata ayıklama için bu kısımları ekleyin
            if not form.is_valid():
                print("Form Hataları:", form.errors)

            if not formset.is_valid():
                for form in formset:
                    if not form.is_valid():
                        print("FormSet Hatası:", form.errors)
            # Hata mesajlarını kullanıcıya göster
    else:
        form = FiyatlandirmaForm(instance=fiyatlandirma)
        formset = FiyatlandirmaItemFormSet(instance=fiyatlandirma)

    context = {
        'form': form,
        'formset': formset,
        'title': 'Fiyatlandırmayı Düzenle'
    }
    return render(request, 'fiyatlandirma.html', context)

@login_required
def cari(request):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    sirketler = Supplier.objects.filter(company=sirket).order_by('name')

    context = {
        'title': 'Cariler',  # Buraya bir virgül eklendi
        'sirketler': sirketler,
        'cari' : True
    }
    return render(request, 'tour/cari.html', context)
@login_required
def cari_islem(request, tedarikci_id, ay_id=None):
    import datetime
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    supplier = Supplier.objects.get(id=tedarikci_id)

    if ay_id is None:
        month = datetime.datetime.now().month
    else:
        month = int(ay_id)  # ay_id'yi int'e çevir

    # Son üç ayı kontrol etmek için bir döngü kullan
    for i in range(12):
        operation_items = OperationItem.objects.filter(
            company=sirket,
            supplier=supplier,
            day__date__month=month
        ).order_by('day__date')

        if operation_items.exists():  # Eğer kayıt varsa döngüden çık
            break
        else:
            month -= 1  # Kayıt yoksa, bir önceki aya geç
            if month < 1:  # Eğer ay 1'den küçükse, yılı azalt ve ayı 12 yap
                month = 12
    supplier_payments = SupplierPaymentDocument.objects.filter(supplier = supplier, upload_date__month = month)
    activity_total_price = 0
    total_payment_price = 0
    for supplier_payment in supplier_payments:
        print(supplier_payment)
        total_payment_price = total_payment_price + supplier_payment.price
    for operation_item in operation_items:
        print(operation_item)
        activity_total_price = activity_total_price + operation_item.vehicle_price
    context = {
        'operation_items': operation_items,
        'sirket_id' : tedarikci_id,
        'activity_total_price' : activity_total_price,
        'cari' : True,
        'total_payment_price' : total_payment_price,
        'supplier_payments' : supplier_payments
    }
    return render(request, 'tour/partials/tedarikci-isleri.html', context)

@login_required
def activity_cari(request):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    sirketler = ActivitySupplier.objects.filter(company=sirket).order_by('name')

    context = {
        'title': 'Cariler',  # Buraya bir virgül eklendi
        'sirketler': sirketler,
        'activity' : True
    }
    return render(request, 'tour/cari.html', context)
@login_required
def activity_cari_islem(request, tedarikci_id, ay_id=None):
    import datetime
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    activity_cost = ActivitySupplier.objects.get(id=tedarikci_id)
    if ay_id is None:
        month = datetime.datetime.now().month
    else:
        month = int(ay_id)

    for i in range(12):
        operation_items = OperationItem.objects.filter(
            company=sirket,
            activity_cost=activity_cost,
            day__date__month=month
        ).order_by('day__date')
        if operation_items.exists():
            break
        else:
            month -= 1  # Bir önceki aya geç
            if month == 0:  # Ay 0 olursa, önceki yıla geçiş yapılır ve ay 12 yapılır.
                month = 12
    supplier_payments = ActivitySupplierPaymentDocument.objects.filter(supplier = activity_cost, upload_date__month = month)
    activity_total_price = 0
    total_payment_price = 0
    for supplier_payment in supplier_payments:
        print(supplier_payment)
        total_payment_price = total_payment_price + supplier_payment.price
    for operation_item in operation_items:
        activity_total_price = activity_total_price + operation_item.activity_price
    context = {
        'operation_items': operation_items,
        'sirket_id' : tedarikci_id,
        'activity_total_price' : activity_total_price,
        'activity' : True,
        'total_payment_price' : total_payment_price,
        'supplier_payments' : supplier_payments
    }
    return render(request, 'tour/partials/tedarikci-isleri.html', context)

@login_required
def comp_jobs(request):
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    sirketler = BuyerCompany.objects.filter(company=sirket).order_by('name')

    context = {
        'title': 'Tamamlanmış İşler',  # Buraya bir virgül eklendi
        'sirketler': sirketler,
        'comp_jobs' : True
    }
    return render(request, 'tour/cari.html', context)
from django.shortcuts import get_object_or_404
@login_required
def comp_jobs_islem(request, tedarikci_id, ay_id=None):
    import datetime
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    today = datetime.datetime.now().date()
    yesterday = today - timedelta(days=1)

    buyer_company = get_object_or_404(BuyerCompany, id=tedarikci_id)
    if ay_id is None:
        month = datetime.datetime.now().month
    else:
        month = int(ay_id)

    if month == 13:
        operations = Operation.objects.filter(buyer_company=buyer_company, finish__gte=today).order_by('finish')
    else:
        for i in range(12):
            operations = Operation.objects.filter(
                company=sirket,
                buyer_company=buyer_company,
                finish__month=month,
                finish__lte=yesterday
            ).order_by('finish')
            if operations.exists():
                break
            else:
                month -= 1  # Bir önceki aya geç
                if month == 0:  # Ay 0 olursa, önceki yıla geçiş yapılır ve ay 12 yapılır.
                    month = 12

    context = {
        'operations': operations,
        'sirket_id' : tedarikci_id,
        'comp_jobs' : True,
        'comp' : False
    }
    return render(request, 'tour/partials/tedarikci-isleri.html', context)



from django.core.paginator import Paginator

@login_required
def logs(request):
    user = request.user
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    logs = UserActivityLog.objects.filter(company = sirket).exclude(action="Giriş yaptı.").order_by('-timestamp')
    page = Paginator(logs, 50)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {'page' : page, 'title' : 'Loglar', 'login' : False}
    return render(request, 'tour/logs.html', context)

from django.db.models import Q

@login_required
def login_logs(request):
    user = request.user
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    logs = UserActivityLog.objects.filter(Q(action="Giriş yaptı.") | Q(action="Çıkış yaptı."), company=sirket).order_by('-timestamp')
    page = Paginator(logs, 50)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {'page' : page, 'title' : 'Loglar', 'login' : True}
    return render(request, 'tour/logs.html', context)


def update_hotel_list(request):
    # Hotel modelinizin queryset'ini güncelleyecek şekilde ayarlayın
    hotels_queryset = Hotel.objects.all().order_by('name')

    # OperationItemForm'un yeni bir örneğini oluşturun
    # Bu örnekte, form içinde belirli bir alanın (hotel) queryset'ini güncelliyoruz
    form = OperationItemForm()
    form.fields['hotel'].queryset = hotels_queryset

    # HTMX isteği için sadece hotel alanını içeren bir template parçası kullanın
    # Bu template parçası, formun hotel alanını güncelleyen HTMX yanıtını içermelidir
    return render(request, 'tour/partials/operation_item_hotel_field.html', {'form': form})

@login_required
def customer_payment(request):
    user = request.user
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    today = datetime.now().date()

    # 7 gün sonra tarihini hesapla
    seven_days_last = today + timedelta(days=7)

    suppliers = Operation.objects.filter(company=sirket).order_by('ticket')
    form = PaymentDocumentForm()
    if request.method =="POST":
        form = PaymentDocumentForm(request.POST, request.FILES)

        supplier_id = request.POST.get('supplier')
        supplier = get_object_or_404(Operation, id=supplier_id)  # day_id yerine item_id kullanılıyor

        if form.is_valid():
            payment_decument = form.save(commit=False)
            payment_decument.operation = supplier
            payment_decument.save()
        return redirect('customer_payment')
    context={
        'suppliers' : suppliers,
        'form' : form,
        'customer' : True,
        'title' : 'Ödeme Al'
    }
    return render(request, 'tour/payment-add.html', context)

@login_required
def cost_payment(request):
    user = request.user
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    suppliers=Supplier.objects.filter(company=sirket)
    activity_suppliers=ActivitySupplier.objects.filter(company=sirket)
    form = SupplierPaymentDocumentForm()
    if request.method =="POST":
        form = SupplierPaymentDocumentForm(request.POST, request.FILES)

        supplier_id = request.POST.get('supplier')
        supplier = get_object_or_404(Supplier, id=supplier_id)  # day_id yerine item_id kullanılıyor

        if form.is_valid():
            payment_decument = form.save(commit=False)
            payment_decument.supplier = supplier
            payment_decument.save()
        return redirect('cost_payment')
    context={
        'suppliers' : suppliers,
        'form' : form,
        'activity_suppliers' : activity_suppliers,
        'customer' : False,
        'title' : 'Ödeme Yap'
    }
    return render(request, 'tour/payment-add.html', context)

@login_required
def activity_cost_payment(request):
    user = request.user
    requestPersonel = Personel.objects.get(user=request.user)
    sirket = requestPersonel.company
    suppliers=Supplier.objects.filter(company=sirket)
    activity_suppliers=ActivitySupplier.objects.filter(company=sirket)
    form = ActivitySupplierPaymentDocumentForm()
    if request.method =="POST":
        form = ActivitySupplierPaymentDocumentForm(request.POST, request.FILES)

        supplier_id = request.POST.get('supplier')
        supplier = get_object_or_404(ActivitySupplier, id=supplier_id)  # day_id yerine item_id kullanılıyor

        if form.is_valid():
            payment_decument = form.save(commit=False)
            payment_decument.supplier = supplier
            payment_decument.save()
        return redirect('cost_payment')
    context={
        'suppliers' : suppliers,
        'form' : form,
        'activity_suppliers' : activity_suppliers,
        'customer' : False
    }
    return render(request, 'tour/payment-add.html', context)


from django.http import JsonResponse
from .models import Hotel

def get_hotels_json(request):
    hotels = Hotel.objects.all().order_by('name')  # Veya herhangi bir sıralama kriteriniz varsa
    hotel_list = [{'id': hotel.id, 'name': hotel.name} for hotel in hotels]
    return JsonResponse({'hotels': hotel_list})




###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################
