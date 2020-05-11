from django.db import models

class TokenList(models.Model):
    '''
    Definirá os token que serão bloqueados no sistema.
    Tokens que á foram utilizados. Não poderão mais ser autenticados.
    '''
    token = models.TextField()                                                                                                                                                                                                  


# class PerfilList(models.Model): Para os perfils bloqueados temporáriamente

