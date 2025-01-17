from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'id', 'worker', 'accepted_workers', 'client', 'job_category', 'job_id',
            'region', 'city', 'price', 'desc', 'full_desc', 'image', 'work_count',
            'is_finish', 'gender', 'view_count', 'status', 'created_at',
            'latitude', 'longitude'
        ]
