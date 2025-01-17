from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from job.serializer import CategoryJobSerializer, JobSerializer
from .models import Order
from job.models import Region, Job, CategoryJob
from .serializer import OrderSerializer
from django.shortcuts import get_object_or_404


class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobListByCategoryView(APIView):
    def get(self, request, pk):
        category_job = get_object_or_404(CategoryJob, id=pk)
        jobs = Job.objects.filter(category_job=category_job)
        category_serializer = CategoryJobSerializer(category_job, context={'request': request})
        jobs_serializer = JobSerializer(jobs, many=True, context={'request': request})

        result = category_serializer.data
        result['jobs'] = jobs_serializer.data

        return Response(result)


@api_view(['GET'])
def categoryjob_list(request):
    category_jobs = CategoryJob.objects.all()
    serializer = CategoryJobSerializer(category_jobs, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated  # Foydalanuvchi autentifikatsiyasi
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import (ClientRegistrationSerializer, ClientLoginSerializer, ClientPasswordChangeSerializer,
                         ClientDetailSerializer)
from django.contrib.auth import get_user_model
User = get_user_model()


class ClientRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ClientRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client= serializer.save()

        refresh = RefreshToken.for_user(client)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class ClientLoginView(generics.GenericAPIView):
    serializer_class = ClientLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.validated_data

        refresh = RefreshToken.for_user(client)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "client": ClientRegistrationSerializer(client).data,
        }, status=status.HTTP_200_OK)


# parol change class
class ClientPasswordChangeView(generics.GenericAPIView):
    serializer_class = ClientPasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Password updated successfully."})

    def perform_update(self, serializer):
        serializer.save()




# class WorkerProfileListView(APIView):
#     permission_classes = [IsAuthenticated, IsClient]
#
#     def get(self, request):
#         location = request.query_params.get('location')
#         if location:
#             workers = WorkerProfile.objects.filter(user__location__icontains=location)
#         else:
#             workers = WorkerProfile.objects.all()
#
#         serializer = WorkerProfileSerializer(workers, many=True)
#         return Response(serializer.data)
#
#
# class WorkerProfileUpdateView(UpdateAPIView):
#     queryset = WorkerProfile.objects.all()
#     serializer_class = WorkerProfileSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):
#         return self.request.user.worker_profile

class ClientProfileView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = ClientDetailSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response({"detail": "Foydalanuvchi tizimga kirmagan"}, status=401)

