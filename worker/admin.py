from django.contrib import admin

from worker.models import WorkerProfile, ProfilImage


class ProfilImageInline(admin.TabularInline):
    model = ProfilImage
    extra = 1


@admin.register(WorkerProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'description', 'avatar', 'reyting']
    fields = ['fullname_uz', 'fullname_ru', 'fullname_en', 'description_uz', 'description_ru', 'description_en']
    inlines = [ProfilImageInline]
