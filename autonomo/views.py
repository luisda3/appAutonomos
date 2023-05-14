from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login
from .models import UserAutonomoForm, CompanyForm, Company, UserAutonomo, UpdateUserAutonomoForm, Supplier, SupplierForm

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

        company = Company.objects.get(user=request.user.id)

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

        company = Company.objects.get(user=request.user.id)

        return render(request, "autonomo/globalPosition.html", context={"company": company})
    
    return redirect("/accounts/login")

def showProfile(request):

    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
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
                company = Company.objects.get(user=request.user.id)
                return render(request,"users/editProfile.html", context={'form': form, "company": company} )
        user = UserAutonomo.objects.get(dni=request.user.username)
        form = UpdateUserAutonomoForm(instance=user)
        company = Company.objects.get(user=request.user.id)

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

def showSuppliers(request):

    if request.user.is_authenticated:

        suppliers = Supplier.objects.all()
        company = Company.objects.get(user=request.user.id)
        paginator = Paginator(suppliers, per_page=2)
        suppliers_page = paginator.page(1)
        pages_list = []
        for i in range(suppliers_page.paginator.num_pages):
            pages_list.append(i+1)

        return render(request, "autonomo/showSuppliers.html", context={"company": company, "suppliers": suppliers_page, "pages_list": pages_list})
    
    return redirect("/accounts/login")

def showSuppliersPaginate(request, page):

    if request.user.is_authenticated:

        suppliers = Supplier.objects.all()
        company = Company.objects.get(user=request.user.id)
        paginator = Paginator(suppliers, per_page=2)
        suppliers_page = paginator.get_page(page)
        pages_list = []
        for i in range(suppliers_page.paginator.num_pages):
            pages_list.append(i+1)

        return render(request, "autonomo/showSuppliers.html", context={"company": company, "suppliers": suppliers_page, "pages_list": pages_list})
    
    return redirect("/accounts/login")

def createSupplier(request):

    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)

        if request.method == "POST":
            data = request.POST.copy()
            data["company"] = company 
            form = SupplierForm(data)
            if form.is_valid():
                supplier = form.save()
                return redirect("/autonomo/showSupplier/" + str(supplier.id))
            else:
                return render(request, "autonomo/createSupplier.html", context={'form': form} )
        else:
            form = SupplierForm()
            return render(request, "autonomo/createSupplier.html", context={"company": company, "form": form})
        
    return redirect("/accounts/login")

def showSupplier(request, sup_id):

    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
        supplier = Supplier.objects.get(id=sup_id)

        return render(request, "autonomo/showSupplier.html", context={"company": company, "supplier": supplier})

def editSupplier(request, sup_id):
    
    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
        supplier = Supplier.objects.get(id=sup_id)

        if request.method == "POST":
            data = request.POST.copy()
            data['nif'] = supplier.nif
            data["company"] = supplier.company
            form = SupplierForm(data, instance=supplier)
            if form.is_valid():
                supplier = form.save()
                return redirect("/autonomo/showSupplier/" + str(supplier.id))
            else:
                return render(request,"autonomo/editSupplier.html", context={'form': form, "company": company} )
        else:
            form = SupplierForm(instance=supplier)

            return render(request, "autonomo/editSupplier.html", context={"company": company, "form": form})

    return redirect("/accounts/login")