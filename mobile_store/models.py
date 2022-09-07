from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True)

class MobilePhone(models.Model):
    RAM_CHOICES = [
        ("2GB", "2"),
        ("4GB", "4"),
        ("6GB", "6"),
        ("8GB", "8"),
        ("12GB", "12"),
    ]
    DISPLAY_CHOICES = [
        ("LED", "LED"),
        ("IPS", "IPS"),
        ("AMOLED", "AMO"),
        ("sAMOLED", "SAMO"),
    ]
    model_name = models.CharField(max_length=256)
    camera_spec = models.CharField(max_length=64)
    model_ram = models.CharField(max_length=48, choices=RAM_CHOICES)
    model_storage = models.CharField(max_length=48)
    model_display = models.CharField(max_length=64, choices=DISPLAY_CHOICES)
    model_price = models.IntegerField()
    model_seller = models.ForeignKey(to=User, on_delete=models.CASCADE)
    model_image = models.URLField(max_length=400)
    
    def __str__(self):
        return self.model_name
