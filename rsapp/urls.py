from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.auth, name='auth'),
    
    path('analytics/', analytics_view, name='analytics'),

    path('payments/', views.payments, name='payments'),
    path('payments/create/', views.create_payment, name='create_payment'),
    path('payments/edit/<int:bill_id>/', views.edit_payment, name='edit_payment'),
    path('payments/delete/<int:bill_id>/', views.delete_payment, name='delete_payment'),


    path('account/logout', views.logout_, name='logout'),
    path('account', views.account, name='account'),
    
    path('rental/', views.rental_objects, name='rental_objects'),
    path('rental/add/', views.add_rental_space, name='add_rental_space'),
    path('rental/edit/<int:pk>/', views.edit_rental_space, name='edit_rental_space'),
    path('rental/delete/<int:pk>/', views.delete_rental_space, name='delete_rental_space'),

    path('contracts/', views.contracts, name='contracts'),
    path('contracts/delete/<int:pk>/', views.delete_contract, name='delete_contract'),
    
    path('create_agreement/', views.create_agreement, name='create_agreement'),
    path('add_tenant_modal/', views.add_tenant_modal, name='add_tenant_modal'),
    
    path('settings/', views.settings, name='settings'),

    path('buildings/', buildings, name='buildings'),
    path('buildings/add/', add_building, name='add_building'),
    path('buildings/edit/<int:building_id>/', edit_building, name='edit_building'),
    path('buildings/delete/<int:building_id>/', delete_building, name='delete_building'),
    
    path('managers/', views.managers, name='managers'),
    path('add_manager/', views.add_manager, name='add_manager'),
    path('edit_manager/<int:pk>/', views.edit_manager, name='edit_manager'),
    path('delete_manager/<int:pk>/', views.delete_manager, name='delete_manager'),

    path('tenants/', views.tenant_list, name='tenant_list'),
    path('tenants/add/', views.tenant_add, name='tenant_add'),
    path('tenants/edit/<int:tenant_id>/', views.tenant_edit, name='tenant_edit'),
    path('tenants/delete/<int:tenant_id>/', views.tenant_delete, name='tenant_delete'),


    path('bills/', views.bills_view, name='bills'),
    path('bills/add/', views.add_bill_view, name='add_bill'),
    path('bills/edit/<int:bill_id>/', views.edit_bill_view, name='edit_bill'),
    path('bills/delete/<int:bill_id>/', views.delete_bill_view, name='delete_bill'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
