from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from accounts.models import Users, EmployeeInfo, UserInfo, Project
from django.contrib import messages
from django.db.models import Q
from accounts.permission import permission_required, has_permission
# Create your views here.
@permission_required('employees','can_add')
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
    'can_view_company': has_permission(request,'companies','can_view'),
    'can_view_employee' : has_permission(request,'employees','can_view'),
    'can_view_lead'     : has_permission(request,'leads','can_view'),
    'can_view_project'  : has_permission(request,'projects','can_view'),
    'can_view_reminder' : has_permission(request,'reminders','can_view'),

}
    return render(request,"employee/add_employee.html",context)

@permission_required('employees','can_delete')
def delete_employee(request,id):
    employee=EmployeeInfo.objects.get(id=id)
    employee.user.delete()
    return redirect('employee_details')

@permission_required('employees','can_edit')
def edit_employee(request, id):
    role = Users.objects.get(user=request.user).role
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
    context = {
        'role':role,
        'employee':employee,
    'can_view_company': has_permission(request,'companies','can_view'),
    'can_view_employee' : has_permission(request,'employees','can_view'),
    'can_view_lead'     : has_permission(request,'leads','can_view'),
    'can_view_project'  : has_permission(request,'projects','can_view'),
    'can_view_reminder' : has_permission(request,'reminders','can_view'),
    }
    return render(request, "employee/edit.html",context)

@permission_required('employees','can_view')
def employee_details(request):
    role = Users.objects.get(user=request.user).role
    
    if role == "admin":
        employees = EmployeeInfo.objects.all()
    elif role == "company":
        company = UserInfo.objects.filter(user=request.user).first()
        employees = EmployeeInfo.objects.filter(company=company)
        
    else:
        employees = EmployeeInfo.objects.none()
        
    search = request.GET.get("search")
    if search:
        employees=employees.filter(
            Q(employee_name__icontains=search) |
            Q(user__email__icontains=search) |
            Q(user__userinfo__userid__icontains=search)
        )
    context={
    'employees':employees,
    'role':role,
    'employees': employees,
    
    'can_add_employee':has_permission(request,'employees','can_add'),
    'can_edit_employee':has_permission(request,'employees','can_edit'),
    'can_delete_employee':has_permission(request,'employees','can_delete'),
    'can_view_company': has_permission(request,'companies','can_view'),
    'can_view_employee' : has_permission(request,'employees','can_view'),
    'can_view_lead'     : has_permission(request,'leads','can_view'),
    'can_view_project'  : has_permission(request,'projects','can_view'),
    'can_view_reminder' : has_permission(request,'reminders','can_view'),
    }
    return render(request,'employee/details.html',context)

@permission_required('projects','can_view')
def project(request):
    role=Users.objects.get(user=request.user).role
    projects=Project.objects.all()
    context = {
        'role':role,
        'projects':projects,
        'can_edit_project':has_permission(request,'projects','can_edit'),
        'can_delete_project':has_permission(request,'projects','can_delete'),
        'can_add_project':has_permission(request,'projects','can_add'),
    'can_view_company': has_permission(request,'companies','can_view'),
    'can_view_employee' : has_permission(request,'employees','can_view'),
    'can_view_lead'     : has_permission(request,'leads','can_view'),
    'can_view_project'  : has_permission(request,'projects','can_view'),
    'can_view_reminder' : has_permission(request,'reminders','can_view'),
    }
    return render(request,"project/project.html",context)

@permission_required('projects','can_add')
def add_project(request):
    role = Users.objects.get(user=request.user).role
    employees=EmployeeInfo.objects.all()
    company = UserInfo.objects.filter(user = request.user).first()
    if request.method == "POST":
        project_name        = request.POST.get("project_name")
        client_name         = request.POST.get("client_name")
        start_date          = request.POST.get("start_date") or None
        end_date            = request.POST.get("end_date") or None
        priority            = request.POST.get("priority")
        status              = request.POST.get("status")
        project_description = request.POST.get("project_description")
        assign_to           = EmployeeInfo.objects.filter(id=request.POST.get("assign_to")).first()
        
        Project.objects.create(
            company             = company,
            project_name        = project_name,
            client_name         = client_name,
            start_date          = start_date,
            end_date            = end_date,
            assign_to           = assign_to,
            priority            = priority,
            status              = status,
            project_description = project_description,
        )
        messages.success(request,"Project Added Successfully")
        return redirect('add_project')
    context = {
        'employees':employees,
        'role':role,
        'can_view_company': has_permission(request,'companies','can_view'),
    'can_view_employee' : has_permission(request,'employees','can_view'),
    'can_view_lead'     : has_permission(request,'leads','can_view'),
    'can_view_project'  : has_permission(request,'projects','can_view'),
    'can_view_reminder' : has_permission(request,'reminders','can_view'),
    }
    return render(request,"project/add_project.html",context)

@permission_required('projects','can_delete')
def delete_project(request,project_id):
    Project.objects.get(project_id = project_id).delete()
    messages.success(request,"project deleted")
    return redirect('project')

@permission_required('projects','can_edit')
def edit_project(request,project_id):
    role = Users.objects.get(user=request.user).role
    project=Project.objects.filter(project_id=project_id).first()
    employees = EmployeeInfo.objects.all()
    if request.method == "POST":
        project.project_name = request.POST.get("project_name")
        project.client_name = request.POST.get("client_name")
        project.start_date = request.POST.get("start_date") or None
        project.end_date = request.POST.get("end_date") or None
        project.assign_to = EmployeeInfo.objects.get(id=request.POST.get("assign_to"))
        project.priority = request.POST.get("priority")
        project.status = request.POST.get("status")
        project.project_description = request.POST.get("project_description")
        project.save()
        messages.success(request,"Project Updated Successfully")
        return redirect('edit_project',project_id=project.project_id)
    context = {
        'project':project,
        'employees':employees,
        'role':role,
        'can_view_company': has_permission(request,'companies','can_view'),
    'can_view_employee' : has_permission(request,'employees','can_view'),
    'can_view_lead'     : has_permission(request,'leads','can_view'),
    'can_view_project'  : has_permission(request,'projects','can_view'),
    'can_view_reminder' : has_permission(request,'reminders','can_view'),
    }
    return render(request,"project/edit_project.html",context)

@permission_required('projects','can_view')
def project_details(request,project_id):
    role = Users.objects.get(user=request.user).role
    project = Project.objects.filter(project_id=project_id).first()
    context={
        'role' : role,
        'project': project,
        'can_view_company': has_permission(request,'companies','can_view'),
    'can_view_employee' : has_permission(request,'employees','can_view'),
    'can_view_lead'     : has_permission(request,'leads','can_view'),
    'can_view_project'  : has_permission(request,'projects','can_view'),
    'can_view_reminder' : has_permission(request,'reminders','can_view'),
    }
    return render(request,"project/project_details.html",context)