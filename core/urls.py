from django.contrib import admin
from django.urls import path
from TourManager.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),
    path('logout/', logout, name='logout'),


    
    path('vehicle/', vehicle, name='vehicle'),
    path('create_vehicle/', create_vehicle, name='create_vehicle'),
    path('delete_vehicle/<int:vehicle_id>/', delete_vehicle, name='delete_vehicle'),
    path('edit_vehicle/<int:vehicle_id>/', edit_vehicle, name='edit_vehicle'),
    path('cancel_vehicle/<int:vehicle_id>/', cancel_vehicle, name='cancel_vehicle'),

    
    path('transfer/', transfer, name='transfer'),
    path('create_transfer/', create_transfer, name='create_transfer'),
    path('delete_transfer/<int:transfer_id>/', delete_transfer, name='delete_transfer'),
    path('edit_transfer/<int:transfer_id>/', edit_transfer, name='edit_transfer'),
    path('cancel_transfer/<int:transfer_id>/', cancel_transfer, name='cancel_transfer'),

    
    path('tour/', tour, name='tour'),
    path('create_tour/', create_tour, name='create_tour'),
    path('delete_tour/<int:tour_id>/', delete_tour, name='delete_tour'),
    path('edit_tour/<int:tour_id>/', edit_tour, name='edit_tour'),
    path('cancel_tour/<int:tour_id>/', cancel_tour, name='cancel_tour'),

    
    path('guide/', guide, name='guide'),
    path('create_guide/', create_guide, name='create_guide'),
    path('delete_guide/<int:guide_id>/', delete_guide, name='delete_guide'),
    path('edit_guide/<int:guide_id>/', edit_guide, name='edit_guide'),
    path('cancel_guide/<int:guide_id>/', cancel_guide, name='cancel_guide'),

    
    path('activity/', activity, name='activity'),
    path('create_activity/', create_activity, name='create_activity'),
    path('delete_activity/<int:activity_id>/', delete_activity, name='delete_activity'),
    path('edit_activity/<int:activity_id>/', edit_activity, name='edit_activity'),
    path('cancel_activity/<int:activity_id>/', cancel_activity, name='cancel_activity'),

    
    path('personel/', personel, name='personel'),
    path('create_personel/', create_personel, name='create_personel'),
    path('delete_personel/<int:personel_id>/', delete_personel, name='delete_personel'),
    path('edit_personel/<int:personel_id>/', edit_personel, name='edit_personel'),
    path('cancel_personel/<int:personel_id>/', cancel_personel, name='cancel_personel'),

    
    path('museum/', museum, name='museum'),
    path('create_museum/', create_museum, name='create_museum'),
    path('delete_museum/<int:museum_id>/', delete_museum, name='delete_museum'),
    path('edit_museum/<int:museum_id>/', edit_museum, name='edit_museum'),
    path('cancel_museum/<int:museum_id>/', cancel_museum, name='cancel_museum'),

    
    path('buyer/', buyer, name='buyer'),
    path('create_buyer/', create_buyer, name='create_buyer'),
    path('delete_buyer/<int:buyer_id>/', delete_buyer, name='delete_buyer'),
    path('edit_buyer/<int:buyer_id>/', edit_buyer, name='edit_buyer'),
    path('cancel_buyer/<int:buyer_id>/', cancel_buyer, name='cancel_buyer'),

    
    path('cost/', cost, name='cost'),
    path('create_cost/', create_cost, name='create_cost'),
    path('delete_cost/<int:cost_id>/', delete_cost, name='delete_cost'),
    path('edit_cost/<int:cost_id>/', edit_cost, name='edit_cost'),
    path('cancel_cost/<int:cost_id>/', cancel_cost, name='cancel_cost'),

    
    path('supplier/', supplier, name='supplier'),
    path('create_supplier/', create_supplier, name='create_supplier'),
    path('delete_supplier/<int:supplier_id>/', delete_supplier, name='delete_supplier'),
    path('edit_supplier/<int:supplier_id>/', edit_supplier, name='edit_supplier'),
    path('cancel_supplier/<int:supplier_id>/', cancel_supplier, name='cancel_supplier'),

    
    path('activity_supplier/', activity_supplier, name='activity_supplier'),
    path('create_activity_supplier/', create_activity_supplier, name='create_activity_supplier'),
    path('delete_activity_supplier/<int:supplier_id>/', delete_activity_supplier, name='delete_activity_supplier'),
    path('edit_activity_supplier/<int:supplier_id>/', edit_activity_supplier, name='edit_activity_supplier'),
    path('cancel_activity_supplier/<int:supplier_id>/', cancel_activity_supplier, name='cancel_activity_supplier'),

    
    path('hotel/', hotel, name='hotel'),
    path('create_hotel/', create_hotel, name='create_hotel'),
    path('delete_hotel/<int:hotel_id>/', delete_hotel, name='delete_hotel'),
    path('edit_hotel/<int:hotel_id>/', edit_hotel, name='edit_hotel'),
    path('cancel_hotel/<int:hotel_id>/', cancel_hotel, name='cancel_hotel'),
    
    
    path('operation/', operation, name='operation'),
    path('operation_list/', operation_list, name='operation_list'),
    path('create_operation/', create_operation, name='create_operation'),
    path('create_operation_item_add/', create_operation_item_add, name='create_operation_item_add'),
    path('create_operation_item/<int:day_id>/', create_operation_item, name='create_operation_item'),
]
