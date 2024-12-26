from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated  # Foydalanuvchi autentifikatsiyasi
from rest_framework_simplejwt.tokens import RefreshToken
from job.models import Job, CategoryJob
from job.serializer import JobSerializer, CategoryJobSerializer
from .serializers import WorkerRegistrationSerializer, WorkerLoginSerializer, \
    WorkerPasswordChangeSerializer, WorkerSerializer, UserUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import AbstractUser
from django.contrib.auth import get_user_model

User = get_user_model()


# def websocket_test(request):
#     return render(request, 'web.html')


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


class JobListByCategoryView(APIView):
    def get(self, request, pk):
        category_job = get_object_or_404(CategoryJob, id=pk)
        jobs = Job.objects.filter(category_job=category_job)
        category_serializer = CategoryJobSerializer(category_job, context={'request': request})
        jobs_serializer = JobSerializer(jobs, many=True, context={'request': request})

        result = category_serializer.data
        result['jobs'] = jobs_serializer.data

        return Response(result)


class UpdateUserJobView(UpdateAPIView):
    queryset = AbstractUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Foydalanuvchi faqat o'zini yangilashi mumkin
        return self.request.user


@api_view(['GET'])
def categoryjob_list(request):
    category_jobs = CategoryJob.objects.all()
    serializer = CategoryJobSerializer(category_jobs, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
