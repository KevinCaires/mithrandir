from django.db import models
from login.models import User

class TokenBlackList(models.Model):
    token_list = models.TextField(
        null=False,
        blank=False,
    )
