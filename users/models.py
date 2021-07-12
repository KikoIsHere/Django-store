from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    is_normal = models.BooleanField(default=False)
    is_legal = models.BooleanField(default=False)

class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    adress = models.CharField(max_length=50,)
    region = models.CharField(max_length=50,)
    city = models.CharField(max_length=50,)
    zip_code = models.CharField(max_length=50,) 
    phone = models.CharField(unique=True, max_length=50)
    club_card = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class LegalAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    adress = models.CharField(max_length=50,)
    region = models.CharField(max_length=50,)
    city = models.CharField(max_length=50,)
    zip_code = models.CharField(max_length=50,) 
    phone = models.CharField(unique=True, max_length=50)
    club_card = models.CharField(max_length=50)
    mol = models.CharField(max_length=50)
    eik = models.CharField(max_length=50)
    dds_number = models.CharField(max_length=50)
    tax_address = models.CharField(max_length=50) 
    
    def __str__(self):
        return self.user.username