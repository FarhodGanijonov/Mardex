from django.urls import path


from .views import OrderListView, OrderDetailView, ClientDetailView
from .views import OrderListView, OrderDetailView, newsclient_list

from django.conf import settings
from django.conf.urls.static import static
from .views import ClientRegistrationView, ClientLoginView, ClientPasswordChangeView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('clientnews/', newsclient_list),
    path('register/', ClientRegistrationView.as_view(), name='client-register'),
    path('login/', ClientLoginView.as_view(), name='client-login'),
    path('password-change/', ClientPasswordChangeView.as_view(), name='client-password-change'),
    path('profiles/', ClientDetailView.as_view(), name='client-detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
