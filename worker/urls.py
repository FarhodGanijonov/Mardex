from django.urls import path
from .views import WorkerRegistrationView, WorkerLoginView, WorkerPasswordChangeView, \
    JobListByCategoryView, categoryjob_list, UpdateUserJobView, OrderStatisticsAPIView, \
    WorkerProfileUpdateView, AddWorkerImageView, DeleteWorkerImageView, WorkerProfileListView, DeleteWorkerImagesView
from .views import (RegionListByCityView, DeleteAllWorkerImagesView, WorkerJobListView,
                    WorkerPhoneUpdateView, JobSearchAPIView, workernews_list)


urlpatterns = [
    path('register/', WorkerRegistrationView.as_view(), name='worker-register'),
    path('login/', WorkerLoginView.as_view(), name='worker-login'),
    path('password-change/', WorkerPasswordChangeView.as_view(), name='worker-password-change'),
    # path('websocket/', websocket_test, name='websocket_test'),

    path('categoryjob_list/', categoryjob_list, name='categoryjob_list'),
    path('category_jobs/<int:pk>/', JobListByCategoryView.as_view(), name='jobs_by_category'),

    # worker ishni update va get qilishi uchun url
    path('update_user_job/', UpdateUserJobView.as_view(), name='jobs_by_category'),
    path('user_job/', WorkerJobListView.as_view(), name='user_job'),  # Profilni ko‘rish uchun API

    # worker profil uchun statistika yani atmen qilingan joblar soni
    path('order-statistics/', OrderStatisticsAPIView.as_view(), name='order-statistics'),

    path('api/worker/update-phone/', WorkerPhoneUpdateView.as_view(), name='worker-update-phone'),

    path('api/city/<int:pk>/', RegionListByCityView.as_view(), name='region-list-by-city'),


    path('worker-job-search/', JobSearchAPIView.as_view(), name='job-search'),
    path('workernews/', workernews_list),



    path('workers/', WorkerProfileListView.as_view(), name='worker-profile-list'),
    # Update Worker Profile
    path('workers/profile/update/', WorkerProfileUpdateView.as_view(), name='worker-profile-update'),
    # Add Worker Image
    path('workers/profile/add-image/', AddWorkerImageView.as_view(), name='add-worker-image'),
    # Delete Worker Image
    path('workers/profile/delete-image/<int:image_id>/', DeleteWorkerImageView.as_view(), name='delete-worker-image'),
    # Delete All Worker Images
    path('workers/profile/delete-all-images/', DeleteAllWorkerImagesView.as_view(), name='delete-all-worker-images'),

    path('delete-images/', DeleteWorkerImagesView.as_view(), name='delete-images'),

]
