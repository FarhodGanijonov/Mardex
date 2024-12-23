# from rest_framework import serializers
# from .models import CategoryJob, Job, City, Region, Proba
#
#
# class CategoryJobSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CategoryJob
#         fields = ['id', 'title', 'image', 'created_at']
#
#
# class JobSerializer(serializers.ModelSerializer):
#     category_job = CategoryJobSerializer()  # Nested serializer
#
#     class Meta:
#         model = Job
#         fields = ['id', 'title', 'category_job', 'image', 'created_at']
#
#
# class CitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = City
#         fields = ['id', 'title']
#
#
# class RegionSerializer(serializers.ModelSerializer):
#     city_id = CitySerializer()
#
#     class Meta:
#         model = Region
#         fields = ['id', 'title', 'city_id']
#
#
