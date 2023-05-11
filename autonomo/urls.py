from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signUp, name="sign up"),
    path("autonomo/", views.autonomo, name="autonomo"),
    path("", views.main, name="main"),
    path("global/", views.globalPosition, name="global"),
    path("accounts/showProfile", views.showProfile, name="showProfile"),
    path("accounts/editProfile", views.editProfile, name="editProfile"),
    path("accounts/showCompany", views.showCompany, name="showCompany"),
    path("accounts/editCompany", views.editCompany, name="editCompany"),
]