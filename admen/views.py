from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from accounts.models import UserInfo, Users
from django.contrib import messages
# Create your views here.
def add_company(request):
    if request.method=="POST":
        company_name =  request.POST.get("company_name")
        email        =  request.POST.get("email")
        address      =  request.POST.get("address")
        gst_no       =  request.POST.get("gst")
        password     =  request.POST.get("password")
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect('add_company')
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        Users.objects.create(
            user=user,
            role="company"
        )
        UserInfo.objects.create(
            user=user,
            company_name=company_name,
            address=address,
            gst=gst_no,
        )
        messages.success(request, "Company added successfully")
        return redirect('add_company')
    companies = UserInfo.objects.filter(user__users__role="company")
    role = Users.objects.get(user=request.user).role
    context={
        'companies':companies,
        'role':role,
    }
    return render(request,"company/add_company.html",context)

def delete_company(request,id):
    company=UserInfo.objects.get(id=id)
    company.user.delete()
    return redirect('company_details')

def edit_company(request,id):
    company=UserInfo.objects.get(id=id)
    if request.method =="POST":
        company.company_name =  request.POST.get("company_name")
        company.address      =  request.POST.get("address")
        company.gst          =  request.POST.get("gst")
        
        email                =  request.POST.get("email")
        password             =  request.POST.get("password")
        
            # 🔹 email duplicate check (FIXED)
        if User.objects.filter(username=email).exclude(id=company.user.id).exists():
            messages.error(request, "Email already exists")
            return redirect('edit_company', id=id)
        
        company.user.email   =  email
        company.user.username=  email
        
        if password:
            company.user.set_password(password)
        
        company.user.save()
        company.save()
        return redirect('company_details')
    return render(request,'company/edit.html',{'company':company})

def company_details(request):
    companies = UserInfo.objects.filter(user__users__role="company")
    role = Users.objects.get(user=request.user).role
    context={
        'companies':companies,
        'role':role,
    }
    return render(request,'company/details.html',context)