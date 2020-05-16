from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    username = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=20,
    )
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
    )
    password = models.CharField(
        null=False,
        blank=False,
        max_length=50,
    )
    cpf = models.CharField(
        null=False,
        blank=False,
        unique=False,
        max_length=20,
    )
    token = models.CharField(
        null=True,
        max_length=300,
    )
    worker = models.BooleanField(
        default=False,
    )

    class Meta:
        permissions = [
            ('suport_user', 'Can edit informations and logins.'),
            ('common_user', 'Common permissions.'),
            ('worker_user', 'Can workon with a job type.'),
        ]