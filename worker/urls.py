from django.urls import path
from .views import WorkerRegistrationView, WorkerLoginView, WorkerPasswordChangeView, WorkerDetailView, \
    JobListByCategoryView, categoryjob_list, UpdateUserJobView, OrderStatisticsAPIView, \
    WorkerProfileUpdateView, AddWorkerImageView, DeleteWorkerImageView, WorkerProfileListView, \
    DeleteAllWorkerImagesView, WorkerJobListView

urlpatterns = [
    path('register/', WorkerRegistrationView.as_view(), name='worker-register'),
    path('login/', WorkerLoginView.as_view(), name='worker-login'),
    path('password-change/', WorkerPasswordChangeView.as_view(), name='worker-password-change'),

    path('worker/<int:id>/', WorkerDetailView.as_view(), name='worker-detail'),

    # path('websocket/', websocket_test, name='websocket_test'),

    path('categoryjob_list/', categoryjob_list, name='categoryjob_list'),
    path('category_jobs/<int:pk>/', JobListByCategoryView.as_view(), name='jobs_by_category'),

    # worker ishni update va get qilishi uchun url
    path('update_user_job/', UpdateUserJobView.as_view(), name='jobs_by_category'),
    path('user_job/', WorkerJobListView.as_view(), name='user_job'),  # Profilni ko‘rish uchun API

    # worker profil uchun statistika yani atmen qilingan joblar soni
    path('order-statistics/', OrderStatisticsAPIView.as_view(), name='order-statistics'),

    # worker profile uchun viewset desa ham bo'ladi.
    path('worker-profiles/', WorkerProfileListView.as_view(), name='list-worker-profiles'),
    path('worker-profiles/<int:profile_id>/images/add/', AddWorkerImageView.as_view(), name='add-worker-image'),
    path('worker-profiles/images/delete/<int:image_id>/', DeleteWorkerImageView.as_view(), name='delete-worker-image'),
    path('worker-profiles/images/delete/all/', DeleteAllWorkerImagesView.as_view(), name='delete-all-worker-images'),
    path('worker-profiles/<int:pk>/update/', WorkerProfileUpdateView.as_view(), name='update-worker-profile'),

]
