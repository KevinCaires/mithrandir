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
        null=False,
        default=False,
    )
    job_group = models.ForeignKey(
        'JobGroup',
        null=False,
        on_delete=models.CASCADE,
    )


class JobGroup(models.Model):
    """
    Grupos de serviço.
    Para identificar em qual grupo um determinado serviço faz parte.
    """
    name = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=50,
    )
    description = models.TextField(
        null=False,
        blank=False,
    )


# class PersonalProtectiveEquipment(models.Model):
#     """
#     Equipamento de proteção individual.
#     É obrigatório que os usuário prestadores dos serviços tenham o próprio equipamento.
#     """
#     name = models.CharField(
#         null=False,
#         blank=False,
#         unique=True,
#         max_length=50,
#     )
#     description = models.TextField(
#         null=False,
#         blank=False,
#     )


# class JobEquipment(models.Model):
#     """
#     Equipamentos necessários para que a atividade possa ser prestada.
#     """
