from typing import Any
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your models here.

class UserAutonomo(User):

    dni = models.CharField(max_length=10)
    birthdate = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)



class UserAutonomoForm(UserCreationForm):

    class Meta():
        model = UserAutonomo
        fields = ["username", "first_name", "last_name", "dni", "birthdate", "address", "city", "email", "password1", "password2"]

class Company(models.Model):

    nif = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    