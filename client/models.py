from django.db import models
from job.models import CategoryJob, Job, Region, City
from users.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
User = get_user_model()


class Order(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Erkak'),
        ('Female', 'Ayol'),
    ]

    STATUS_CHOICES = [
        ('stable', 'Stable'),
        ('success', 'Success'),
        ('cancel_client', 'Cancel by Client'),
        ('cancel_user', 'Cancel by User'),
    ]

    worker = models.ForeignKey(AbstractUser, on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='orders_as_worker')
    accepted_workers = models.ManyToManyField(AbstractUser, related_name='accepted_orders', blank=True)
    client = models.ForeignKey(AbstractUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='client')
    job_category = models.ForeignKey(CategoryJob, on_delete=models.SET_NULL, blank=True, null=True)
    job_id = models.ManyToManyField(Job, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    desc = models.TextField(default="", blank=True, null=True)
    full_desc = models.TextField(default="", blank=True, null=True)
    image = models.ImageField(upload_to='client_image/', blank=True, null=True)
    work_count = models.IntegerField(default=1)
    is_finish = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    view_count = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='stable'
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.client} by {self.worker}"


class ClientReyting(models.Model):

    active_orders = models.PositiveIntegerField(default=0)  # Faol buyurtmalar soni
    completed_orders = models.PositiveIntegerField(default=0)  # Bajarilgan buyurtmalar soni
    cancelled_orders = models.PositiveIntegerField(default=0)  # Bekor qilingan buyurtmalar soni
    reyting = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(100.0)

        ], default=0.0,)

