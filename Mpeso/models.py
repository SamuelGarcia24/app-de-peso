from django.db import models
from django.contrib.auth.models import User

class UserPeso(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pesoIdeal = models.IntegerField(null=False, blank=False)
    altura = models.IntegerField(null=False, blank=False)
    
class PesoActual(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pesoActual = models.IntegerField(null=False, blank=False)
