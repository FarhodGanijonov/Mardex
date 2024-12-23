# from rest_framework import serializers
# from .models import AbstractUser
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
#
#
# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = AbstractUser
#         fields = [
#             'id', 'role', 'gender', 'full_name', 'phone', 'password', 'region', 'city',
#             'passport_scan', 'passport_back_scan', 'passport_scan_with_face',
#             'passport_seria', 'job_category', 'job_id', 'avatar',
#             'description', 'is_staff', 'is_superuser', 'is_active',
#             'is_online', 'created_at'
# ]
#
#
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         return token
