from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import UserAutonomoForm, CompanyForm, Company, UserAutonomo, UpdateUserAutonomoForm

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
            return render(request,"users/signup.html", context={'form': form} )
    
    form = UserAutonomoForm()
    return render(request, "users/signup.html", context={"form": form})

def autonomo(request):

    if request.user.is_authenticated:

        company = Company.objects.filter(user=request.user.id)

        if request.method == "POST":
            data = request.POST.copy()
            data['user'] = request.user
            form = CompanyForm(data)
            if form.is_valid():
                form.save()
                return redirect("/global")
            else:
                return render(request, "autonomo/index.html", context={"form": form})
        elif company:
            return redirect("/global")
        else:
            form = CompanyForm()
            return render(request, "autonomo/index.html", context={"form": form})
    else:
        return redirect("/accounts/login")

def globalPosition(request):
    
    if request.user.is_authenticated:

        company = Company.objects.filter(user=request.user)

        return render(request, "autonomo/globalPosition.html", context={"company": company})
    
    return redirect("/accounts/login")

def showProfile(request):

    if request.user.is_authenticated:
        company = Company.objects.filter(user=request.user)
        users = UserAutonomo.objects.filter(dni=request.user.username)

        return render(request, "users/showProfile.html", context={"company": company, "autonomo": users[0]})
    
    return redirect("/accounts/login")

def editProfile(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            user = UserAutonomo.objects.get(dni=request.user.username)

            form = UpdateUserAutonomoForm(request.POST, instance=request.user)
            if form.is_valid():
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.birthdate = request.POST["birthdate"]
                user.address = request.POST["address"]
                user.city = request.POST["city"]
                user.save()
                return redirect("/account/showProfile")
            else:
                company = Company.objects.filter(user=request.user)
                return render(request,"users/editProfile.html", context={'form': form, "company": company} )
        user = UserAutonomo.objects.get(dni=request.user.username)
        form = UpdateUserAutonomoForm(instance=user)
        company = Company.objects.filter(user=request.user)

        return render(request, "users/editProfile.html", context={"company": company, "form": form})
    
    return redirect("/accounts/login")

def showCompany(request):
    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)

        return render(request, "autonomo/showCompany.html", context={"company": company})
    
    return redirect("/accounts/login")

def editCompany(request):
    
    if request.user.is_authenticated:
        if request.method == "POST":
            company = Company.objects.get(user=request.user.id)
            data = request.POST.copy()
            data['nif'] = company.nif
            data['user'] = request.user

            form = CompanyForm(data, instance=company)
            if form.is_valid():
                form.save()
                return redirect("/account/showCompany")
            else:
                return render(request,"autonomo/editCompany.html", context={'form': form, "company": company} )
        else:
            company = Company.objects.get(user=request.user.id)
            form = CompanyForm(instance=company)

            return render(request, "autonomo/editCompany.html", context={"company": company, "form": form})

    return redirect("/accounts/login")
