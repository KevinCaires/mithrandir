from django.db import models
from login.models import User
from jobs.models import Job

class UserProfile(models.Model):
    photo_profile = models.ImageField(
        upload_to='user_profiles',
    )
    name = models.CharField(
        blank=False,
        null=False,
        max_length=20,
    )
    last_name = models.CharField(
        blank=False,
        null=False,
        max_length=20,
    )
    birth_date = models.DateField(
        blank=False,
        null=False,
    )
    certificate = models.ImageField(
        upload_to='user_profiles',
    )
    criminal_record = models.ImageField(
        upload_to='user_profiles',
    )
    phone_ddi_1 = models.CharField(
        blank=False,
        null=False,
        max_length=2,
    )
    phone_number_1 = models.CharField(
        blank=False,
        null=False,
        max_length=11,
        unique=True,
    )
    phone_ddi_2 = models.CharField(
        max_length=2,
    )
    phone_number_2 = models.CharField(
        blank=True,
        null=True,
        max_length=11,
        unique=True,
    )
    user = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE,
    )
    jobs = models.ManyToManyField(
        Job,
        blank=True,
    )
