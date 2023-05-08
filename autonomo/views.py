from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import UserAutonomoForm

# Create your views here.
def main(request):
    return render(request, "users/main.html")

def signUp(request):

    if request.method == "POST":
        data = request.POST.copy()
        data['username'] = data['dni']
        form = UserAutonomoForm(data)
        if form.is_valid():
            autonomo = form.save()
            login(request, autonomo)
            return redirect("/autonomo")
        else:
            return HttpResponse(form.errors.values())
    
    form = UserAutonomoForm()
    return render(request, "users/signup.html", context={"form": form})

def autonomo(request):

    # Si tiene negocios creados va a la pantalla de su negocio

    # Si no tiene negocios va a la pantalla de crear negocios
    if request.user.is_authenticated:

        return render(request, "autonomo/index.html")
    else:
        return redirect("/accounts/login")
