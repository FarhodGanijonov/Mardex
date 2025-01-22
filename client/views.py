from rest_framework.decorators import api_view
from .models import Order, ClientNews
from .serializer import OrderSerializer, ClientNewsSerializer, ClientDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import ClientRegistrationSerializer, ClientLoginSerializer, ClientPasswordChangeSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


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


@api_view(['GET'])
def newsclient_list(request):
    news = ClientNews.objects.all()
    serializer = ClientNewsSerializer(news, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
