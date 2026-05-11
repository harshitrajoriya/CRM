from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from accounts.models import Users, EmployeeInfo, UserInfo
from django.contrib import messages
# Create your views here.
def add_employee(request):
    company=UserInfo.objects.get(user=request.user)
    employees = EmployeeInfo.objects.filter(company=company)
    role = Users.objects.get(user=request.user).role
    if request.method=="POST":
        employee_name     = request.POST.get("Employee_name")
        employee_email    = request.POST.get("email")
        employee_phone    = request.POST.get("phone")
        employee_address  = request.POST.get("address")
        employee_password = request.POST.get("password")
        employee_dob      = request.POST.get("dob")
        employee_doj      = request.POST.get("doj")
        employee_salary   = request.POST.get("salary")
        
        if User.objects.filter(email=employee_email).exists():
            messages.error(request, "Email already exists")
            return redirect('add_employee')
        
        user=User.objects.create_user(
            username=employee_email,
            email=employee_email,
            password=employee_password
        )
        Users.objects.create(
            user=user,
            phone=employee_phone,
            role="employee"
        )
        UserInfo.objects.create(user=user)
        EmployeeInfo.objects.create(
            user=user,
            company=company,
            employee_name=employee_name,
            address=employee_address,
            dob=employee_dob,
            doj=employee_doj,
            salary=employee_salary
        )
        messages.success(request, "Employee added successfully")
        return redirect('add_employee')
    context={
    'employees':employees,
    'role':role,
}
    return render(request,"employee/add_employee.html",context)

def delete_employee(request,id):
    employee=EmployeeInfo.objects.get(id=id)
    employee.user.delete()
    return redirect('employee_details')

def edit_employee(request, id):
    employee = EmployeeInfo.objects.get(id=id)

    if request.method == "POST":
        employee.employee_name = request.POST.get("Employee_name")
        employee.address = request.POST.get("address")
        employee.dob = request.POST.get("dob")
        employee.doj = request.POST.get("doj")
        employee.salary = request.POST.get("salary")

        # 🔹 update phone
        user_extra = Users.objects.get(user=employee.user)
        user_extra.phone = request.POST.get("phone")
        user_extra.save()

        # 🔹 update email
        employee_email = request.POST.get("email")

        if User.objects.filter(email=employee_email).exclude(id=employee.user.id).exists():
            messages.error(request, "Email already exists")
            return redirect('edit_employee', id=id)

        employee.user.email = employee_email
        employee.user.username = employee_email

        # 🔹 update password (optional)
        employee_password = request.POST.get("password")
        if employee_password:
            employee.user.set_password(employee_password)

        employee.user.save()
        employee.save()

        return redirect('employee_details')
    
    return render(request, "employee/edit.html", {'employee': employee})

def employee_details(request):
    role = Users.objects.get(user=request.user).role
    
    if role == "admin":
        employees = EmployeeInfo.objects.all()
    elif role == "company":
        company = UserInfo.objects.filter(user=request.user).first()
        employees = EmployeeInfo.objects.filter(company=company)
        
    else:
        employees = EmployeeInfo.objects.none()
        
    context={
    'employees':employees,
    'role':role,
}
    return render(request,'employee/details.html',context)