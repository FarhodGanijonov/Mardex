from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from users.models import AbstractUser

User = get_user_model()


class WorkerProfile(models.Model):
    user = models.OneToOneField(
        AbstractUser,
        on_delete=models.CASCADE,
        null=True,
        related_name='worker_profile'
    )
    fullname = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='worker_image/', blank=True, null=True)
    reyting = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(100.0)
        ],
        default=0.0
    )

    def __str__(self):
        return self.fullname or "Worker Profile"


class ProfilImage(models.Model):
    profile = models.ForeignKey(
        WorkerProfile,
        on_delete=models.CASCADE,
        related_name='profileimage',
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to='wor_image/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check if the profile already has 5 images
        if self.profile and self.profile.profileimage.count() >= 5:
            raise ValidationError("Profilda 5 tadan ortiq rasm boʻlishi mumkin emas.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.profile}" if self.profile else "No profile"


# Signal to create a WorkerProfile automatically when a user is created
@receiver(post_save, sender=AbstractUser)
def create_worker_profile(sender, instance, created, **kwargs):
    if created:
        WorkerProfile.objects.create(user=instance)

#
# class WorkerTariff(models.Model):
#     name = models.CharField(max_length=100)  # Tarif nomi, masalan, "Tekin", "Start", "Active"
#     price = models.PositiveIntegerField(default=0)  # Tarif narxi (so'mda)
#     top_limit = models.PositiveIntegerField()  # Necha marta "top" qilish imkoniyati
#     call_limit = models.PositiveIntegerField()  # Necha marta "vizov" qilish imkoniyati
#
#
#     def __str__(self):
#         return f"{self.name} - {self.price} so'm"
#
#     class Meta:
#         verbose_name = "Worker Tarif"
#         verbose_name_plural = "Worker Tariflar"
#
#
# class TarifHaridi(models.Model):
#     user = models.ForeignKey(
#         AbstractUser,
#         on_delete=models.CASCADE,
#         null=True,
#         related_name='worker_harid')
#     tarif_id = models.ForeignKey(WorkerTariff, on_delete=models.CASCADE,null=True)
#     status = models.BooleanField(default=True)


class WorkerNews(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='workernews_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
