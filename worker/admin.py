from django.contrib import admin
from worker.models import WorkerNews, WorkerImage
from django.contrib.auth import get_user_model

User = get_user_model()


class WorkerImageInline(admin.TabularInline):
    model = WorkerImage
    extra = 1


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'role', 'gender', 'phone', 'is_superuser',]
    list_filter = ['role', 'gender', 'created_at']
    search_fields = ['full_name_uz', 'full_name_ru', 'full_name_en', 'phone',]
    fields = [
        'full_name_uz', 'full_name_ru', 'full_name_en',
        'description_uz', 'description_ru', 'description_en',
        'gender'
    ]
    inlines = [WorkerImageInline]


@admin.register(WorkerNews)
class WorkerNewsAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'description')
    fields = ['description_uz', 'description_ru', 'description_en', 'image',]
    ordering = ('created_at',)
