# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.views import TokenObtainPairView
#
# from users.models import AbstractUser
# from users.serializer import CustomTokenObtainPairSerializer, UserSerializer
#
#
# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
#
#
# class ProtectedView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         return Response({"message": "Siz autentifikatsiya qildingiz!"})
#
#
# class RegisterAPIView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = AbstractUser.objects.create_user(
#                 phone=serializer.validated_data['phone'],
#                 full_name=serializer.validated_data['full_name'],
#                 password=serializer.validated_data['password']
#             )
#             return Response({"message": "Foydalanuvchi muvaffaqiyatli yaratildi."})
#         return Response(serializer.errors)
