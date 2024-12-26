from django.urls import path
from .views import WorkerRegistrationView, WorkerLoginView, WorkerPasswordChangeView, WorkerDetailView, \
    JobListByCategoryView, categoryjob_list, UpdateUserJobView, OrderStatisticsAPIView

urlpatterns = [
    path('register/', WorkerRegistrationView.as_view(), name='worker-register'),
    path('login/', WorkerLoginView.as_view(), name='worker-login'),
    path('password-change/', WorkerPasswordChangeView.as_view(), name='worker-password-change'),

    path('worker/<int:id>/', WorkerDetailView.as_view(), name='worker-detail'),

    # path('websocket/', websocket_test, name='websocket_test'),

    path('categoryjob_list/', categoryjob_list, name='categoryjob_list'),
    path('category_jobs/<int:pk>/', JobListByCategoryView.as_view(), name='jobs_by_category'),

    path('update_user_job/', UpdateUserJobView.as_view(), name='jobs_by_category'),
    path('order-statistics/', OrderStatisticsAPIView.as_view(), name='order-statistics'),

]
