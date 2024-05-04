# In serializers.py
from rest_framework import serializers
from .models import Vendor
from .models import PurchaseOrder
from .models import VendorPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        # fields = ['name', 'vendor_code']
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPerformance
        fields = '__all__'