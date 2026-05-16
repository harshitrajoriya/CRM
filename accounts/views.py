from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from accounts.models import Users, UserInfo, EmployeeInfo
# Create your views here.
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user_obj = User.objects.filter(email=email).first()

        if not user_obj:
            messages.error(request, "User not found")
            return redirect('login')

        user = authenticate(request, username=user_obj.username, password=password)

        if user is None:
            messages.error(request, "Invalid password")
            return redirect('login')

        login(request, user)
        return redirect('dashboard')

    return render(request, "login.html")

def dashboard(request):
    user            = request.user   
    user_role       = Users.objects.filter(user=user).first()
    companies       = UserInfo.objects.filter(user__users__role="company")
    role            = user_role.role if user_role else None
    companies_count = companies.count()
    employees_count = EmployeeInfo.objects.count()
    company = None
    
    if role == "company":
        company=UserInfo.objects.filter(user=request.user).first()
        
    context = {
        "user": user,
        "role": role,
        
        'companies': companies,
        'company'  : company,
        
        'companies_count':companies_count,
        'employees_count':employees_count
    }
    return render(request,"dashboard.html",context)

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')

