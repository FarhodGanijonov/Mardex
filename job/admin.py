from django.contrib import admin
from .models import CategoryJob, Job, City, Region


@admin.register(CategoryJob)
class CategoryJobAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    fields = ['title_uz', 'title_ru', 'title_en',]
    ordering = ('created_at',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_job', 'created_at')
    search_fields = ('title',)
    fields = ['title_uz', 'title_ru', 'title_en', 'category_job',]
    ordering = ('created_at',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    fields = ['title_uz', 'title_ru', 'title_en',]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('title', 'city_id')
    search_fields = ('title',)
    fields = ['title_uz', 'title_ru', 'title_en', 'city_id']
    ordering = ('title',)


