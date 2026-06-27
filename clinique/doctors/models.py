from django.db import models

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    office = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr {self.first_name} {self.last_name}"