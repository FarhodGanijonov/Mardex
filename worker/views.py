from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated  # Foydalanuvchi autentifikatsiyasi
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q

from client.models import Order
from job.models import Job, CategoryJob
from job.serializer import JobSerializer, CategoryJobSerializer
from .models import WorkerProfile, ProfilImage
from .permissions import IsClient
from .serializers import WorkerRegistrationSerializer, WorkerLoginSerializer, \
    WorkerPasswordChangeSerializer, WorkerSerializer, UserUpdateSerializer, WorkerProfileSerializer, \
    WorkerImageSerializer, WorkerJobSerializer, WorkerPhoneUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import AbstractUser
from django.contrib.auth import get_user_model
from job.models import City, Region
from .serializers import CitySerializer, RegionSerializer



User = get_user_model()


# def websocket_test(request):
#     return render(request, 'web.html')

# registratsiya qismi class
class WorkerRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = WorkerRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        worker = serializer.save()

        refresh = RefreshToken.for_user(worker)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


# login class
class WorkerLoginView(generics.GenericAPIView):
    serializer_class = WorkerLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        worker = serializer.validated_data

        refresh = RefreshToken.for_user(worker)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "worker": WorkerRegistrationSerializer(worker).data,
        }, status=status.HTTP_200_OK)

# parol change class
class WorkerPasswordChangeView(generics.GenericAPIView):
    serializer_class = WorkerPasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Password updated successfully."})

    def perform_update(self, serializer):
        serializer.save()


# workerlarni barcha malumotlarini olish
class WorkerDetailView(generics.RetrieveAPIView):
    serializer_class = WorkerSerializer

    def get_queryset(self):
        # Faqat 'role=worker' bo'lgan foydalanuvchilarni filtrlash
        return User.objects.filter(role='worker')

    def get(self, request, *args, **kwargs):
        worker_id = kwargs.get('id')
        # Filtrlashdan so'ng foydalanuvchini olish
        worker = get_object_or_404(self.get_queryset(), id=worker_id)
        serializer = self.get_serializer(worker)
        return Response(serializer.data)


# category bo'yicha job larni filterlash
class JobListByCategoryView(APIView):
    def get(self, request, pk):
        category_job = get_object_or_404(CategoryJob, id=pk)
        jobs = Job.objects.filter(category_job=category_job)
        category_serializer = CategoryJobSerializer(category_job, context={'request': request})
        jobs_serializer = JobSerializer(jobs, many=True, context={'request': request})

        result = category_serializer.data
        result['jobs'] = jobs_serializer.data

        return Response(result)


# worker uchun tangalagan ishlarini upfate va get qilish uchun classlar
class UpdateUserJobView(UpdateAPIView):
    queryset = AbstractUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Foydalanuvchi faqat o'zini yangilashi mumkin
        return self.request.user


class WorkerJobListView(RetrieveAPIView):
    queryset = AbstractUser.objects.select_related('job_category').prefetch_related('job_id')  # Optimallashtirish
    serializer_class = WorkerJobSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Faqat kirgan foydalanuvchining ma'lumotlarini qaytaradi


# ishlarni categoriyasi uchun list
@api_view(['GET'])
def categoryjob_list(request):
    category_jobs = CategoryJob.objects.all()
    serializer = CategoryJobSerializer(category_jobs, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# worker profilini statistikasi yani nechta odam atmen qilganligi
class OrderStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        total_orders = Order.objects.filter(worker=user).count()
        success_orders = Order.objects.filter(worker=user, status='success').count()
        cancel_client_orders = Order.objects.filter(worker=user, status='cancel_client').count()

        # Natijalarni JSON formatida qaytarish
        return Response({
            "total_orders": total_orders,
            "success_orders": success_orders,
            "cancel_client_orders": cancel_client_orders,
        })


# worker profil uchun views
class WorkerProfileListView(APIView):
    permission_classes = [IsAuthenticated, IsClient]

    def get(self, request):
        location = request.query_params.get('location')
        if location:
            workers = WorkerProfile.objects.filter(user__location__icontains=location)
        else:
            workers = WorkerProfile.objects.all()

        serializer = WorkerProfileSerializer(workers, many=True)
        return Response(serializer.data)


class WorkerProfileUpdateView(UpdateAPIView):
    queryset = WorkerProfile.objects.all()
    serializer_class = WorkerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.worker_profile


class AddWorkerImageView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, profile_id=None):
        # WorkerProfile ID bo'yicha aniqlash
        try:
            profile = WorkerProfile.objects.get(id=profile_id)
        except WorkerProfile.DoesNotExist:
            return Response({"error": "Profil topilmadi."}, status=404)

        # Tasvirlarni 5 tadan oshirmaslikni tekshirish
        if profile.profileimage.count() >= 5:
            return Response({"error": "5 tadan ortiq tasvir qo'shib bo'lmaydi."}, status=400)

        # Tasvirni saqlash
        serializer = WorkerImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DeleteWorkerImageView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, image_id):
        image = ProfilImage.objects.filter(id=image_id, profile=request.user.worker_profile).first()
        if image:
            image.delete()
            return Response({"message": "Tasvir o'chirildi."}, status=204)
        return Response({"error": "Tasvir topilmadi."}, status=404)


class DeleteAllWorkerImagesView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        profile = request.user.worker_profile
        profile.profileimage.all().delete()
        return Response({"message": "Barcha tasvirlar o'chirildi."}, status=204)


class WorkerPhoneUpdateView(generics.GenericAPIView):
    serializer_class = WorkerPhoneUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Phone number updated successfully."}, status=status.HTTP_200_OK)


class RegionListByCityView(APIView):

    def get(self, request, pk):
        # Shaharning `id`si bo‘yicha City modelini topamiz
        city = get_object_or_404(City, id=pk)

        # Ushbu shaharga tegishli Regionlarni olish
        regions = Region.objects.filter(city_id=city)

        # Serializerlar bilan ma'lumotlarni formatlaymiz
        city_serializer = CitySerializer(city, context={'request': request})
        regions_serializer = RegionSerializer(regions, many=True, context={'request': request})

        # Natijani birlashtirib qaytaramiz
        result = city_serializer.data
        result['regions'] = regions_serializer.data

        return Response(result)


class JobSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')

        if not query:
            return Response({"error": "Qidiruv so'rovini kiriting (q)"},)

        # Harflar bo'yicha qidiruv
        categories = CategoryJob.objects.filter(title__icontains=query)
        jobs = Job.objects.filter(Q(title__icontains=query) | Q(category_job__title__icontains=query))

        category_serializer = CategoryJobSerializer(categories, many=True, context={'request': request})
        job_serializer = JobSerializer(jobs, many=True, context={'request': request})

        return Response({
            "categories": category_serializer.data,
            "jobs": job_serializer.data
        })

