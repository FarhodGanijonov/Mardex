from django.contrib import admin
from .models import CategoryJob, Job, City, Region


@admin.register(CategoryJob)
class CategoryJobAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    ordering = ('created_at',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_job', 'created_at')
    search_fields = ('title',)
    ordering = ('created_at',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('title', 'city_id')
    search_fields = ('title',)
    ordering = ('title',)


