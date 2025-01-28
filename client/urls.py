from django.urls import path



from .views import OrderListView, OrderDetailView, ClientDetailView, ClientNewsDetailView, OrderCreateView
from .views import OrderListView, OrderDetailView, newsclient_list

from .views import (
    OrderListView,
    OrderDetailView,
    JobListByCategoryView,
    categoryjob_list,
    newsclient_list,
    TarifHaridiCreateView,
    ClientRegistrationView,
    ClientLoginView,
    ClientPasswordChangeView,
    clienttarif_list,
    tarif_list,
    ClientListView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('orderscreate/', OrderCreateView.as_view(), name='order-create'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('clientnews/', newsclient_list),
    path('register/', ClientRegistrationView.as_view(), name='client-register'),
    path('login/', ClientLoginView.as_view(), name='client-login'),
    path('password-change/', ClientPasswordChangeView.as_view(), name='client-password-change'),
    path('profiles/', ClientDetailView.as_view(), name='client-detail'),

    path('tarifharid/', TarifHaridiCreateView.as_view(), name='tarif-harid'),
    path('clientnews/', newsclient_list),
    path('clientnews/<int:pk>/', ClientNewsDetailView.as_view(), name='newsclient-detail'),
    path('clienttariflist/', clienttarif_list),
    path('tarif/', tarif_list),
    path('clients/', ClientListView.as_view(), name='client-list'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
