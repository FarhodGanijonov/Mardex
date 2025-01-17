from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'worker', 'job_category', 'region', 'city', 'price', 'status', 'created_at')
    fields = ['client', 'worker', 'accepted_workers', 'job_category', 'job_id', 'city', 'region', 'price',
              'desc', 'full_desc', 'work_count', 'gender', 'status', 'is_finish', 'latitude', 'longitude']
    ordering = ('created_at',)
