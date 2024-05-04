from django.urls import path, include

from . import views
from .views import *

urlpatterns = [
    # path("", pages),
    path("", views.index, name="index"),
    path("vendor/", views.post_vendor, name="post_vendor"),
    path("vendor/<int:vendor_id>/", views.retrieve_vendor, name="retrieve_vendor"),
    path("vendor/<int:vendor_id>/update/", views.update_vendor, name="update_vendor"),
    path("vendor/<int:vendor_id>/delete/", views.delete_vendor, name="delete_vendor"),


    # for purchase orders
    path('purchase-orders/', views.purchase_order, name='purchase-order-list'),
    path('purchase-orders/create/', views.create_purchase_order, name='purchase-order-create'),
    path('purchase-orders/<str:po_number>/', views.retrieve_purchase_order, name='purchase-order-detail'),
    path('purchase-orders/<str:po_number>/update/', views.update_purchase_order, name='purchase-order-update'),
    path('purchase-orders/<str:po_number>/delete/', views.delete_purchase_order, name='purchase-order-delete'),


    # from vendor performance
    path("performance/", views.vendor_performance, name="vendor_performance"),

    path('purchase-orders/create/', views.create_purchase_order, name='purchase-order-create'),
    path('vendor-performances/', views.list_vendor_performance, name='vendor-performance-list'),


     path('vendors/<int:vendor_id>/performance/', views.get_vendor_performance, name='get_vendor-performance'),
    path('purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order, name='acknowledge-purchase-order'),
    
]