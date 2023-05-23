from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist

from .models import UserAutonomoForm, CompanyForm, Company, UserAutonomo, UpdateUserAutonomoForm, Supplier, SupplierForm, Product, ProductForm, Invoice, InvoiceForm, InvoiceLineForm, InvoiceLine, AccountingYear

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

        if request.method == "POST":
            data = request.POST.copy()
            data['user'] = request.user
            form = CompanyForm(data)
            if form.is_valid():
                form.save()
                return redirect("/global")
            else:
                return render(request, "autonomo/index.html", context={"form": form})
        else:
            try:
                company = Company.objects.get(user=request.user.id)
                return redirect("/global")
            except ObjectDoesNotExist:
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
        user = UserAutonomo.objects.get(dni=request.user.username)

        try:
            company = Company.objects.get(user=request.user.id)
        except ObjectDoesNotExist:
            return render(request, "users/showProfile2.html", context={"autonomo": user})

        return render(request, "users/showProfile.html", context={"company": company, "autonomo": user})
    
    return redirect("/accounts/login")

def editProfile(request):

    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
        user = UserAutonomo.objects.get(dni=request.user.username)

        if request.method == "POST":

            form = UpdateUserAutonomoForm(request.POST)
            if form.is_valid():
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.birthdate = request.POST["birthdate"]
                user.address = request.POST["address"]
                user.city = request.POST["city"]
                user.save()
                return redirect("/accounts/showProfile")
            else:
                return render(request,"users/editProfile.html", context={'form': form, "company": company})
            
        form = UpdateUserAutonomoForm(instance=user)

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
                return redirect("/autonomo/showCompany")
            else:
                return render(request,"autonomo/editCompany.html", context={'form': form, "company": company} )
        else:
            company = Company.objects.get(user=request.user.id)
            form = CompanyForm(instance=company)

            return render(request, "autonomo/editCompany.html", context={"company": company, "form": form})

    return redirect("/accounts/login")

def showSuppliers(request):

    if request.user.is_authenticated:

        company = Company.objects.get(user=request.user.id)
        suppliers = Supplier.objects.filter(company=company.id)

        paginator = Paginator(suppliers, per_page=2)
        suppliers_page = paginator.page(1)
        pages_list = []
        for i in range(suppliers_page.paginator.num_pages):
            pages_list.append(i+1)

        return render(request, "autonomo/showSuppliers.html", context={"company": company, "suppliers": suppliers_page, "pages_list": pages_list})
    
    return redirect("/accounts/login")

def showSuppliersPaginate(request, page):

    if request.user.is_authenticated:

        company = Company.objects.get(user=request.user.id)
        suppliers = Supplier.objects.filter(company=company.id)

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

def showProducts(request):

    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)

        products = Product.objects.filter(company=company.id)
        paginator = Paginator(products, per_page=4)
        products_page = paginator.page(1)
        pages_list = []
        for i in range(products_page.paginator.num_pages):
            pages_list.append(i+1)

        return render(request, "autonomo/showProducts.html", context={"company": company, "products": products_page, "pages_list": pages_list})
    
    return redirect("/accounts/login")

def showProductsPaginate(request, page):

    if request.user.is_authenticated:

        company = Company.objects.get(user=request.user.id)
        products = Product.objects.filter(company=company.id)
        paginator = Paginator(products, per_page=4)
        products_page = paginator.get_page(page)
        pages_list = []
        for i in range(products_page.paginator.num_pages):
            pages_list.append(i+1)

        return render(request, "autonomo/showProducts.html", context={"company": company, "products": products_page, "pages_list": pages_list})
    
    return redirect("/accounts/login")

def createProduct(request):

    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)

        if request.method == "POST":
            data = request.POST.copy()
            data["company"] = company 
            form = ProductForm(data, request.FILES)
            print(form.errors)
            if form.is_valid():
                product = form.save()
                return redirect("/autonomo/showProduct/" + str(product.id))
            else:
                return render(request, "autonomo/createProduct.html", context={"company": company, 'form': form} )
        else:
            form = ProductForm()
            return render(request, "autonomo/createProduct.html", context={"company": company, "form": form})
        
    return redirect("/accounts/login")

def showProduct(request, prod_id):

    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
        product = Product.objects.get(id=prod_id)

        return render(request, "autonomo/showProduct.html", context={"company": company, "product": product})

def editProduct(request, prod_id):
    
    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
        product = Product.objects.get(id=prod_id)

        if request.method == "POST":
            data = request.POST.copy()
            data["company"] = company.id
            form = ProductForm(data, instance=product)
            if form.is_valid():
                product = form.save()
                return redirect("/autonomo/showProduct/" + str(product.id))
            else:
                return render(request,"autonomo/editProduct.html", context={'form': form, "company": company} )
        else:
            form = ProductForm(instance=product)

            return render(request, "autonomo/editProduct.html", context={"company": company, "form": form})

    return redirect("/accounts/login")

def deleteProduct(request, prod_id):
    if request.user.is_authenticated:
        Product.objects.get(id=prod_id).delete()
        return redirect("/autonomo/showProducts")
    
    return redirect("/accounts/login")

def deleteSupplier(request, sup_id):
    if request.user.is_authenticated:
        Supplier.objects.get(id=sup_id).delete()
        return redirect("/autonomo/showSuppliers")
    
    return redirect("/accounts/login")

def createInvoice(request):
    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
        if request.method == "POST":
            data = request.POST.copy()
            data["subtotal"] = 0.0
            data["iva"] = 0.0
            data["total"] = 0.0
            data_split = str(data["invoicing_date"]).split("-")
            try:
                year = AccountingYear.objects.get(year=data_split[0], company=company.id)
            except ObjectDoesNotExist:
                year = AccountingYear(year=data_split[0], company=company)
                year.save()
            data["accounting_year"] = year
            form = InvoiceForm(data)
            if form.is_valid():
                invoice = form.save()
                return redirect("/autonomo/showInvoice/"+str(invoice.id))
            else:
                return render(request, "autonomo/createInvoice.html", context={"company": company, "form": form})
        else:
            form = InvoiceForm()
            return render(request, "autonomo/createInvoice.html", context={"company": company, "form": form})
    
    else:
        return redirect("accounts/login")
    
def showInvoice(request, inv_id):

    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)

        invoice = Invoice.objects.get(id=inv_id)
            
        lines = InvoiceLine.objects.filter(invoice=inv_id)

        return render(request, "autonomo/showInvoice.html", context={"company": company, "invoice": invoice, "lines": lines})

def createInvoiceLine(request, inv_id):

    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
        if request.method == "POST":
            data = request.POST.copy()
            data["invoice"] = inv_id
            product = Product.objects.get(id=data["product"])
            data["subtotal"] = int(data["quantity"]) * product.sale_price
            data["iva"] = round(float(int(data["quantity"]) * (product.sale_price * (product.iva/100))),2)
            form = InvoiceLineForm(data)
            if form.is_valid():
                line = form.save()
                invoice = Invoice.objects.get(id=inv_id)
                invoice.subtotal += line.subtotal
                invoice.iva += line.iva
                invoice.total = invoice.subtotal + invoice.iva
                invoice.save()
                return redirect("/autonomo/showInvoice/" + str(inv_id))
            else:
                return render(request, "/autonomo/createInvoiceLine.html", context={"company": company, "form": form})
        else:
            form = InvoiceLineForm()
            return render(request, "autonomo/createInvoiceLine.html", context={"company": company, "form": form})
    else:
        return redirect("accounts/login")
    
def showInvoices(request):

    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
        accountyear = AccountingYear.objects.filter(company=company.id)
        invoices = Invoice.objects.none()
        for year in accountyear:
            invoicess = Invoice.objects.filter(accounting_year=year.id)
            invoices = invoices | invoicess

        paginator = Paginator(invoices, per_page=2)
        invoices_page = paginator.page(1)
        pages_list = []
        for i in range(invoices_page.paginator.num_pages):
            pages_list.append(i+1)

        return render(request, "autonomo/showInvoices.html", context={"company": company, "invoices": invoices_page, "pages_list": pages_list})
    
    return redirect("/accounts/login")


def showInvoicesPaginate(request, page):

    if request.user.is_authenticated:

        company = Company.objects.get(user=request.user.id)
        accountyear = AccountingYear.objects.filter(company=company.id)
        invoices = Invoice.objects.none()
        for year in accountyear:
            invoicess = Invoice.objects.filter(accounting_year=year.id)
            invoices = invoices | invoicess
            
        paginator = Paginator(invoices, per_page=2)
        invoices_page = paginator.page(page)
        pages_list = []
        for i in range(invoices_page.paginator.num_pages):
            pages_list.append(i+1)

        return render(request, "autonomo/showInvoices.html", context={"company": company, "invoices": invoices_page, "pages_list": pages_list})
    
    return redirect("/accounts/login")

def showAccountingYears(request):

    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
        accountyear = AccountingYear.objects.filter(company=company.id)
        paginator = Paginator(accountyear, per_page=4)
        accountyear_page = paginator.page(1)
        pages_list = []
        for i in range(accountyear_page.paginator.num_pages):
            pages_list.append(i+1)

        return render(request, "autonomo/showAccountingYears.html", context={"company": company, "years": accountyear_page, "pages_list": pages_list})
    
    return redirect("/accounts/login")

def showInvoicesYear(request, year):

    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
        accountyear = AccountingYear.objects.get(company=company.id, year=year)
        invoices = Invoice.objects.filter(accounting_year=accountyear.id)
        paginator = Paginator(invoices, per_page=4)
        invoices_page = paginator.page(1)
        pages_list = []
        for i in range(invoices_page.paginator.num_pages):
            pages_list.append(i+1)

        return render(request, "autonomo/showInvoices.html", context={"company": company, "invoices": invoices_page, "pages_list": pages_list})
    
    return redirect("/accounts/login")

def editInvoiceLine(request, line):
    
    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
        invoice_line = InvoiceLine.objects.get(id=line)
        prod = Product.objects.get(id=invoice_line.product.id)

        if request.method == "POST":
            data = request.POST.copy()
            data["product"] = invoice_line.product
            data["invoice"] = invoice_line.invoice
            data["subtotal"] = int(data["quantity"]) * prod.sale_price
            data["iva"] = int(data["subtotal"]) * (prod.iva / 100)
            form = InvoiceLineForm(data, instance=invoice_line)
            if form.is_valid():
                invoice_line = form.save()
                invoice = Invoice.objects.get(id=invoice_line.invoice.id)
                lines = InvoiceLine.objects.filter(invoice=invoice.id)
                subtotal = 0.0
                iva = 0.0
                for line in lines:
                    iva += line.iva
                    subtotal += line.subtotal

                invoice.subtotal = subtotal
                invoice.iva = iva
                invoice.total = subtotal + iva
                invoice.save()
                return redirect("/autonomo/showInvoice/" + str(invoice_line.invoice.id))
            else:
                return render(request,"autonomo/editInvoiceLine.html", context={'form': form, "company": company} )
        else:
            form = InvoiceLineForm(instance=invoice_line)

            return render(request, "autonomo/editInvoiceLine.html", context={"company": company, "form": form})

    return redirect("/accounts/login")

def deleteInvoiceLine(request, line):
    if request.user.is_authenticated:
        invoice_line = InvoiceLine.objects.get(id=line)
        invoice = Invoice.objects.get(id=invoice_line.invoice.id)

        InvoiceLine.objects.get(id=line).delete()

        lines = InvoiceLine.objects.filter(invoice=invoice.id)
        subtotal = 0.0
        iva = 0.0
        for line in lines:
            iva += line.iva
            subtotal += line.subtotal

        invoice.subtotal = subtotal
        invoice.iva = iva
        invoice.total = subtotal + iva
        invoice.save()
        return redirect("/autonomo/showInvoice/" + str(invoice.id))
    
    return redirect("/accounts/login")

def editInvoice(request, inv_id):
    
    if request.user.is_authenticated:
        company = Company.objects.get(user=request.user.id)
        invoice = Invoice.objects.get(id=inv_id)

        if request.method == "POST":
            data = request.POST.copy()
            data["name"] = invoice.name
            data["subtotal"] = invoice.subtotal
            data["iva"] = invoice.iva
            data["total"] = invoice.total
            data["accounting_year"] = invoice.accounting_year
            form = InvoiceForm(data, instance=invoice)
            if form.is_valid():
                invoice = form.save()

                return redirect("/autonomo/showInvoice/" + str(invoice.id))
            else:
                return render(request,"autonomo/editInvoice.html", context={'form': form, "company": company} )
        else:
            form = InvoiceForm(instance=invoice)

            return render(request, "autonomo/editInvoice.html", context={"company": company, "form": form})

    return redirect("/accounts/login")

def deleteInvoice(request, inv_id):
    if request.user.is_authenticated:

        Invoice.objects.get(id=inv_id).delete()

        return redirect("/autonomo/showInvoices/")
    
    return redirect("/accounts/login")