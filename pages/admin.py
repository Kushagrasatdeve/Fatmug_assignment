from django.contrib import admin
from .models import Vendor, PurchaseOrder, VendorPerformance

admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(VendorPerformance)
