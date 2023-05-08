from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signUp, name="sign up"),
    path("autonomo/", views.autonomo, name="autonomo"),
    path("", views.main, name="main"),
]