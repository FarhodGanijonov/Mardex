
from rest_framework.decorators import api_view
from .models import Order, ClientNews
from .serializer import OrderSerializer, ClientNewsSerializer, ClientDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .models import Order, ClientNews, ClientTarif, TarifHaridi
from job.models import Job, CategoryJob
from .serializer import (
    OrderSerializer,
    ClientNewsSerializer,
    ClientTarifSerializer,
    TarifHaridiSerializer,
    ClientRegistrationSerializer,
    ClientLoginSerializer,
    ClientPasswordChangeSerializer,
)
from job.serializer import CategoryJobSerializer, JobSerializer

User = get_user_model()

### Order Viewlar

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

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

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

### Job Viewlar



class JobListByCategoryView(APIView):
    def get(self, request, pk):
        category_job = get_object_or_404(CategoryJob, id=pk)
        jobs = Job.objects.filter(category_job=category_job)
        category_serializer = CategoryJobSerializer(category_job, context={'request': request})
        jobs_serializer = JobSerializer(jobs, many=True, context={'request': request})

        result = category_serializer.data
        result['jobs'] = jobs_serializer.data

        return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def categoryjob_list(request):
    category_jobs = CategoryJob.objects.all()
    serializer = CategoryJobSerializer(category_jobs, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

### Client Viewlar


class ClientRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ClientRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()

        # Foydalanuvchiga avtomatik 0 so'mlik tarifni bog'lash
        self.assign_default_tarif(client)

        refresh = RefreshToken.for_user(client)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    def assign_default_tarif(self, user):
        default_tarif = ClientTarif.objects.filter(price=0).first()
        if default_tarif:
            TarifHaridi.objects.get_or_create(user=user, tarif_id=default_tarif)

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



class ClientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = request.user
        serializer = ClientDetailSerializer(client, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        client = request.user
        serializer = ClientDetailSerializer(client, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


### News Viewlar


@api_view(['GET'])
def newsclient_list(request):
    news = ClientNews.objects.all()
    serializer = ClientNewsSerializer(news, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

### Tarif Viewlar

class TarifHaridiCreateView(generics.CreateAPIView):
    queryset = TarifHaridi.objects.all()
    serializer_class = TarifHaridiSerializer


@api_view(['GET'])
def clienttarif_list(request):
    # Foydalanuvchini tekshirish
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."},
                        status=status.HTTP_401_UNAUTHORIZED)

    # Tizimga kirgan foydalanuvchining tariflarini olish
    tarif = TarifHaridi.objects.filter(user=request.user)
    serializer = TarifHaridiSerializer(tarif, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def tarif_list(request):
    clienttarif = ClientTarif.objects.all()
    serializer = ClientTarifSerializer(clienttarif, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


class ClientListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ClientRegistrationSerializer