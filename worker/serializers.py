from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import AbstractUser
from job.models import Job, CategoryJob
from worker.models import ProfilImage, WorkerProfile, WorkerNews
from job.models import Region, City

User = get_user_model()


class WorkerRegistrationSerializer(serializers.ModelSerializer):
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

        worker = User(
            phone=validated_data['phone'],
            full_name=validated_data['full_name'],
            region=validated_data.get('region'),
            city=validated_data.get('city'),
            gender=validated_data.get('gender'),
            role="worker"
        )
        worker.set_password(validated_data['password'])
        worker.save()
        return worker


class WorkerLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")
        worker = User.objects.filter(phone=phone).first()

        if worker and worker.check_password(password):
            return worker
        else:
            raise serializers.ValidationError("Invalid phone or password")


class WorkerPasswordChangeSerializer(serializers.Serializer):
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


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar', 'description', 'full_name', 'job_category', 'job_id', 'role']


class UserUpdateSerializer(serializers.ModelSerializer):
    # Bu yerda job_category va job_id ni ID orqali yangilash mumkin
    job_category = serializers.PrimaryKeyRelatedField(queryset=CategoryJob.objects.all())
    job_id = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(),
                                                many=True)  # job_id - bu ManyToManyField, shuning uchun many=True

    class Meta:
        model = AbstractUser  # Bu serializer AbstractUser modeliga tegishli
        fields = ['job_category', 'job_id']  # faqat job_category va job_id ni yangilaymiz

    # Yangilanishni amalga oshirish
    def update(self, instance, validated_data):
        # Yangi job_category va job_id ni olish
        job_category_data = validated_data.get('job_category')
        if job_category_data:
            instance.job_category = job_category_data  # job_category ni yangilash

        job_data = validated_data.get('job_id')
        if job_data:
            instance.job_id.set(job_data)  # job_id (ManyToMany) ni yangilash

        instance.save()
        return instance


class WorkerJobSerializer(serializers.ModelSerializer):
    job_category = serializers.StringRelatedField()  # Kategoriyani matn sifatida qaytaradi
    job_id = serializers.StringRelatedField(many=True)  # Ko'p ishlari (ManyToManyField) matn sifatida

    class Meta:
        model = AbstractUser
        fields = ['id', 'full_name', 'job_category', 'job_id']


class WorkerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilImage
        fields = ['id', 'image']


class WorkerProfileSerializer(serializers.ModelSerializer):
    images = WorkerImageSerializer(many=True, read_only=True)

    class Meta:
        model = WorkerProfile
        fields = ['id', 'fullname', 'description', 'avatar', 'reyting', 'images']


class WorkerPhoneUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_phone = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        if user.role != 'worker':
            raise serializers.ValidationError("Only workers can update their phone number.")
        new_phone = self.validated_data['new_phone']
        user.phone = new_phone
        user.save()
        return user


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'title']  # Kerakli maydonlarni kiriting


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'title',]  # Kerakli maydonlarni kiriting


class WorkerNewsSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = WorkerNews
        fields = ['id', 'description', 'image', 'created_at']
