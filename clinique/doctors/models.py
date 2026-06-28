# d:\ITU\django\clinique\doctors\models.py
from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    office = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr {self.first_name} {self.last_name}"