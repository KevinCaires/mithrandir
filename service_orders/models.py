from django.db import models
from jobs.models import Job

class ServiceOrder(models.Model):
    title = models.CharField(
        null=False,
        blank=False,
        max_length=50,
    )
    description = models.TextField(
        null=False,
        blank=False,
    )
    open_date = models.DateTimeField(
        auto_now_add=True,
    )
    close_date = models.DateTimeField(
        auto_now=False,
        null=True,
    )
    service_value = models.FloatField(
        null=True,
    )
    # Issue # 1
    # job = models.ForeignKey(
    #     Job,
    #     null=False,
    #     on_delete=models.CASCADE
    # )
    per_meter = models.BooleanField(
        null=False,
        blank=False,
        default=False,
    )



class Vote(models.Model):
    vote = models.IntegerField(
        default=0,
    )
    coments = models.TextField(
        null=True,
        blank=False,
    )
    service_order = models.ForeignKey(
        'service_orders.ServiceOrder',
        related_name='votes',
        on_delete=models.CASCADE,
    )
