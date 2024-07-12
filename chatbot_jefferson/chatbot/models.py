# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission

class Questions(models.Model):
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()
    token = models.CharField(max_length=255, blank=True, null=True) 
    

    
