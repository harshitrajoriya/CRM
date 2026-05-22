from django.shortcuts import render, redirect
from accounts.models import Permission, Users
from django.contrib import messages
# Create your views here.

def permission(request):
    # ONLY SUPERADMIN
    role = Users.objects.get(user=request.user).role
    if role != "superadmin":
        return redirect('no_access')
    # ALL ROLES
    roles = [
        'admin',
        'company',
        'employee',
    ]
    # ALL MODULES
    modules = [
        'dashboard',
        'leads',
        'projects',
        'reminders',
        'employees',
        'companies',
        'settings',
        'permissions',
    ]
    # AUTO CREATE PERMISSIONS

    for role in roles:
        for module in modules:
            Permission.objects.get_or_create(role=role,module=module)

    permissions = Permission.objects.all().order_by('role','module')
    context = {'permissions': permissions,}
    return render(request,"role/permission.html",context)


# =========================================
# UPDATE PERMISSION
# =========================================

def update_permission(request, id):
    role = Users.objects.get(user=request.user).role
    # ONLY SUPERADMIN

    if role != "superadmin":
        return redirect('no_access')

    permission = Permission.objects.filter(id=id).first()

    permission.can_view = True if request.POST.get('can_view') else False

    permission.can_add = True if request.POST.get('can_add') else False

    permission.can_edit = True if request.POST.get('can_edit') else False
    permission.can_delete = True if request.POST.get('can_delete') else False
    permission.save()
    
    messages.success(request,"Permission Updated Successfully")
    return redirect('permission')