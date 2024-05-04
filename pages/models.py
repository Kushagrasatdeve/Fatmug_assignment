# In models.py

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Avg, Count, F
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=100)
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    acknowledgment_date = models.DateTimeField(null=True)

    def acknowledge(self):
        self.acknowledgment_date = timezone.now()
        self.save()
        self.calculate_average_response_time()

    def calculate_average_response_time(self):
        acknowledged_orders = PurchaseOrder.objects.filter(vendor=self.vendor, acknowledgment_date__isnull=False)
        if acknowledged_orders.exists():
            response_times = [(order.acknowledgment_date - order.issue_date).total_seconds() for order in acknowledged_orders]
            average_response_time = sum(response_times) / len(response_times)
            self.vendorperformance_set.create(
                date=timezone.now(),
                average_response_time=average_response_time
            )
    

class VendorPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

    def __str__(self):
        return f"{self.vendor} - {self.date}"

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    vendor = instance.vendor

    if instance.status == "completed":
        # Update On-Time Delivery Rate
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status="completed")
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        total_completed_pos = completed_pos.count()

        if total_completed_pos > 0:
            on_time_delivery_rate = on_time_deliveries / total_completed_pos
            VendorPerformance.objects.update_or_create(
                vendor=vendor,
                date=timezone.now(),
                defaults={'on_time_delivery_rate': on_time_delivery_rate}
            )

    if instance.quality_rating is not None:
        # Update Quality Rating Average
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status="completed")
        quality_rating_avg = completed_pos.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']
        VendorPerformance.objects.update_or_create(
            vendor=vendor,
            date=timezone.now(),
            defaults={'quality_rating_avg': quality_rating_avg}
        )

@receiver(pre_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, **kwargs):
    if instance.pk:  # Check if the instance already exists
        try:
            old_instance = PurchaseOrder.objects.get(pk=instance.pk)
            if not old_instance.acknowledgment_date and instance.acknowledgment_date:
                # Update Average Response Time
                response_times = PurchaseOrder.objects.filter(vendor=instance.vendor, acknowledgment_date__isnull=False).exclude(pk=instance.pk).annotate(
                    response_time=F('acknowledgment_date') - F('issue_date')
                ).aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
                VendorPerformance.objects.update_or_create(
                    vendor=instance.vendor,
                    date=timezone.now(),
                    defaults={'average_response_time': response_times}
                )
        except ObjectDoesNotExist:
            pass

@receiver(post_save, sender=PurchaseOrder)
def update_fulfillment_rate(sender, instance, created, **kwargs):
    vendor = instance.vendor
    fulfilled_pos = PurchaseOrder.objects.filter(vendor=vendor, status="completed", issue_date__lte=instance.issue_date)

    total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()

    fulfillment_rate = fulfilled_pos.count() / total_pos if total_pos > 0 else 0

    VendorPerformance.objects.update_or_create(
        vendor=vendor,
        date=timezone.now(),
        defaults={'fulfillment_rate': fulfillment_rate}
    )
