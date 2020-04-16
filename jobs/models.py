from django.db import models

class Job(models.Model):
    """
    Tipos de serviço que um usuário pode participar ou solicitar.
    É recomendado que apenas os administradores possam criar tipos de serviço.
    """
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=50,
    )
    per_meter = models.BooleanField(
        blank=False,
        null=False,
        default=False,
    )
    value_per_meter = models.FloatField(
        null=True,
    )
    job_group = models.CharField(
        blank=False,
        null=False,
        max_length=50,
    )
