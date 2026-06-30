from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('DOCTOR', 'Médecin'),
        ('RECEPTIONIST', 'Réceptionniste'),
        ('CLIENT' , 'client'),
        ('PHARMARMACIST', 'Pharmaceutique')
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CLIENT'
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    photo = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"