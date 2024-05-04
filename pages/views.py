from rest_framework.response import Response
from rest_framework.decorators import api_view


# In views.py
from rest_framework import generics
from .models import Vendor, PurchaseOrder, VendorPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer

@api_view(['GET'])
def index(request):
    vendor_objs = Vendor.objects.all()
    serializer = VendorSerializer(vendor_objs, many = True)
    return Response({'status': 200, 'payload': serializer.data})

@api_view(['POST'])
def post_vendor(request):
    data = request.data
    serializer = VendorSerializer(data = request.data)

    if not serializer.is_valid():
        return Response({'status': 403 , 'message': 'Something went wrong'})
    
    serializer.save()

    return Response({'status': 200, 'payload': serializer.data, 'message' :'you sent'})

@api_view(['GET'])
def retrieve_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'status': 404, 'message': 'Vendor not found'}, status=404)
    serializer = VendorSerializer(vendor)
    return Response({'status': 200, 'payload': serializer.data})

@api_view(['PUT'])
def update_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'status': 404, 'message': 'Vendor not found'}, status=404)
    serializer = VendorSerializer(vendor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 200, 'message': 'Vendor updated successfully'})
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'status': 404, 'message': 'Vendor not found'}, status=404)
    vendor.delete()
    return Response({'status': 204, 'message': 'Vendor deleted successfully'})

@api_view(['GET'])
def purchase_order(request):
    purchase_orders = PurchaseOrder.objects.all()
    serializer = PurchaseOrderSerializer(purchase_orders, many=True)
    return Response({'status': 200, 'payload': serializer.data})

@api_view(['POST'])
def create_purchase_order(request):
    serializer = PurchaseOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 201, 'payload': serializer.data, 'message': 'Purchase Order created successfully'})
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def retrieve_purchase_order(request, po_number):
    try:
        purchase_order = PurchaseOrder.objects.get(po_number=po_number)
    except PurchaseOrder.DoesNotExist:
        return Response({'status': 404, 'message': 'Purchase Order not found'}, status=404)
    serializer = PurchaseOrderSerializer(purchase_order)
    return Response({'status': 200, 'payload': serializer.data})

@api_view(['PUT'])
def update_purchase_order(request, po_number):
    try:
        purchase_order = PurchaseOrder.objects.get(po_number=po_number)
    except PurchaseOrder.DoesNotExist:
        return Response({'status': 404, 'message': 'Purchase Order not found'}, status=404)
    serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 200, 'message': 'Purchase Order updated successfully'})
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_purchase_order(request, po_number):
    try:
        purchase_order = PurchaseOrder.objects.get(po_number=po_number)
    except PurchaseOrder.DoesNotExist:
        return Response({'status': 404, 'message': 'Purchase Order not found'}, status=404)
    purchase_order.delete()
    return Response({'status': 204, 'message': 'Purchase Order deleted successfully'})

@api_view(['GET'])
def vendor_performance(request):
    vendor_performance = VendorPerformance.objects.all()
    serializer = VendorPerformanceSerializer(vendor_performance, many=True)
    return Response({'status': 200, 'payload': serializer.data})

@api_view(['POST'])
def create_purchase_order(request):
    serializer = PurchaseOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # Trigger the update of performance metrics
        serializer.instance.update_performance_metrics()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def list_vendor_performance(request):
    vendor_performances = VendorPerformance.objects.all()
    serializer = VendorPerformanceSerializer(vendor_performances, many=True)
    return Response(serializer.data)


def get_vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=404)

    vendor_performance = VendorPerformance.objects.filter(vendor=vendor)
    serializer = VendorPerformanceSerializer(vendor_performance, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({'error': 'Purchase Order not found'}, status=404)

    purchase_order.acknowledge()
    return Response({'message': 'Purchase Order acknowledged successfully'})
