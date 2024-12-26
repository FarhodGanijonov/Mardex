from rest_framework import serializers
from .models import CategoryJob, Job, City, Region

from rest_framework import serializers
from .models import CategoryJob, Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'image', 'created_at']

class CategoryJobSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True, read_only=True)

    class Meta:
        model = CategoryJob
        fields = ['id', 'title', 'image', 'created_at', 'jobs']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'title']


class RegionSerializer(serializers.ModelSerializer):
    city_id = CitySerializer()

    class Meta:
        model = Region
        fields = ['id', 'title', 'city_id']
