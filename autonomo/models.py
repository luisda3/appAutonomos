from typing import Any, Dict
from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from datetime import date

# Create your models here.

User._meta.get_field('email')._unique = True

class UserAutonomo(User):

    dni = models.CharField(max_length=10, unique=True)
    birthdate = models.DateField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)


class Company(models.Model):
    nif = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    activity = models.CharField(max_length=20)
    foundation_date = models.DateField()
    user = models.OneToOneField(UserAutonomo, on_delete=models.CASCADE, related_name="company_belongs_to")


class DateInput(forms.DateInput):
    input_type = 'date'

class UserAutonomoForm(UserCreationForm):

    class Meta():
        model = UserAutonomo
        widgets = {'birthdate': DateInput()}
        fields = ["username", "first_name", "last_name", "dni", "birthdate", "address", "city", "email", "password1", "password2"]

    def clean(self):
        cleaned_data = super(UserAutonomoForm, self).clean()

        today = date.today()
        age = today.year - cleaned_data["birthdate"].year - ((today.month, today.day) < (cleaned_data["birthdate"].month, cleaned_data["birthdate"].day))
        if age < 18:
            self.add_error("birthdate", "Debes ser mayor de edad para poder registrarte.")
            

class UpdateUserAutonomoForm(ModelForm):

    class Meta():
        model = UserAutonomo
        widgets = {'birthdate': DateInput()}
        fields = ["first_name", "last_name", "birthdate", "address", "city"]

    def clean(self):
        cleaned_data = super(UserAutonomoForm, self).clean()

        today = date.today()
        age = today.year - cleaned_data["birthdate"].year - ((today.month, today.day) < (cleaned_data["birthdate"].month, cleaned_data["birthdate"].day))
        if age < 18:
            self.add_error("birthdate", "Debes ser mayor de edad.")
            
    
class CompanyForm(ModelForm):

    class Meta():
        model = Company
        widgets = {'foundation_date': DateInput()}
        fields = "__all__"
        
    def clean(self):
        cleaned_data = super(CompanyForm, self).clean()

        today = date.today()
        if cleaned_data["foundation_date"] > today:
            self.add_error("foundation_date", "La fecha de fundación no puede ser posterior a la fecha actual.")


class Product(models.Model):
    cod = models.IntegerField()
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    cost_price = models.FloatField()
    sale_price = models.FloatField()
    stock_min = models.IntegerField()
    iva = models.IntegerField()
    image = models.ImageField(upload_to = 'images/')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_belongs_to")


class ProductForm(ModelForm):
    
    class Meta():
        model = Product
        fields = "__all__"


class Supplier(models.Model):
    nif = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="supplier_belongs_to")


class SupplierForm(ModelForm):

    class Meta():
        model = Supplier
        fields = "__all__"
