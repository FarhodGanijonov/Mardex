from rest_framework import serializers
<<<<<<< HEAD
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
=======
from django.contrib.auth import get_user_model
User = get_user_model()


class ClientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone', 'password', 'password_confirmation', 'region', 'city', 'gender']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        # Parol tasdiqlash maydonini o'chirish
        validated_data.pop('password_confirmation')

        client = User(
            phone=validated_data['phone'],
            full_name=validated_data['full_name'],
            region=validated_data.get('region'),
            city=validated_data.get('city'),
            gender=validated_data.get('gender'),
            role="client"
        )
        client.set_password(validated_data['password'])
        client.save()
        return client


class ClientLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")
        client = User.objects.filter(phone=phone).first()

        if client and client.check_password(password):
            return client
        else:
            raise serializers.ValidationError("Invalid phone or password")


class ClientPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
>>>>>>> aa2505376e5c615e6f22ca7055eb00927ea3a686
