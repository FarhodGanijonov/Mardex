from django.urls import path
from .views import ClientRegistrationView, ClientLoginView, ClientPasswordChangeView

urlpatterns = [
    path('register/', ClientRegistrationView.as_view(), name='client-register'),
    path('login/', ClientLoginView.as_view(), name='client-login'),
    path('password-change/', ClientPasswordChangeView.as_view(), name='client-password-change'),
]