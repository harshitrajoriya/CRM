from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from accounts.models import *
from django.contrib import messages
from django.db.models import Q
from datetime import date, timedelta
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
    
    search = request.GET.get("search")
    if search:
        companies=companies.filter(
            Q(company_name__icontains = search) |
            Q(user__email__icontains = search) |
            Q(gst__icontains = search)
        )
    context={
        'companies':companies,
        'role':role,
    }
    return render(request,'company/details.html',context)

def leads(request):
    role = Users.objects.get(user=request.user).role
    employees = EmployeeInfo.objects.all()

    leads = Leads.objects.all().order_by('-id')
    search = request.GET.get("search")
    if search:
        leads = leads.filter(
            Q(lead_name__icontains = search) |
            Q(lead_email__icontains = search)
        )
    context={
        'role':role,
        'employees':employees,
        'leads':leads,
    }
    return render(request,"leads/leads.html",context)

def add_leads(request):
    company = UserInfo.objects.filter(user=request.user).first()
    role = Users.objects.get(user=request.user).role
    employees = EmployeeInfo.objects.all()
    types = ForType.objects.all()
    sources = Leadsource.objects.all()
    statuses = LeadStatus.objects.filter(leadstatus_status = 'active')
    
    if request.method == "POST":
        company_name     = request.POST.get("company_name")
        lead_name        = request.POST.get("lead_name")
        lead_phone       = request.POST.get("lead_phone")
        lead_email       = request.POST.get("lead_email")
        
        lead_status      = LeadStatus.objects.get(id=request.POST.get("Status"))
        lead_source      = Leadsource.objects.get(id=request.POST.get("lead_source"))
        for_type         = ForType.objects.get(id=request.POST.get("for_type"))
        
        from_assign_user = EmployeeInfo.objects.filter(id= request.POST.get("from_assign_user")).first()
        to_assign_user   = EmployeeInfo.objects.filter(id= request.POST.get("to_assign_user")).first()
        
        Leads.objects.create(
            company          = company,
            company_name     = company_name,
            lead_name        = lead_name,
            lead_phone       = lead_phone,
            lead_email       = lead_email,
            from_assign_user = from_assign_user,
            to_assign_user   = to_assign_user,
            lead_source      = lead_source,
            for_type         = for_type,
            status           = lead_status,
        )
        messages.success(request,"Lead added successfully")
        return redirect('leads')
    context = {
        'employees': employees,
        'role': role,
        'types':types,
        'sources':sources,
        'statuses':statuses,
    }
    return render(request,"leads/add_leads.html",context)

def delete_lead(request,id):
    Leads.objects.get(id=id).delete()
    messages.success(request,"Lead deleted successfully")
    return redirect('leads')

def lead_source(request):
    role = Users.objects.get(user=request.user).role
    sources=Leadsource.objects.all()
    context={
        'role':role,
        'sources':sources,
    }
    return render(request,"leads/lead_source.html",context)

def add_lead_source(request):
    role=Users.objects.get(user=request.user).role
    if request.method == "POST":
        lead_source_name = request.POST.get("lead_source_name")
        lead_status = request.POST.get("lead_status")
        Leadsource.objects.create(
            lead_source_name=lead_source_name,
            lead_status=lead_status
        )
        messages.success(request,"Source Added Successfully")
        return redirect('lead_source')
    context ={
        'role':role,
    }
    return render(request,"leads/add_lead_source.html",context)

def delete_lead_source(request,id):
    Leadsource.objects.get(id=id).delete()
    messages.success(request,"Source deleted successfully")
    return redirect('lead_source')

def inactive_lead_source(request, id):
    source = Leadsource.objects.get(id=id)
    source.lead_status = "inactive"
    source.save()
    return redirect('lead_source')


def active_lead_source(request, id):
    source = Leadsource.objects.get(id=id)
    source.lead_status = "active"
    source.save()
    return redirect('lead_source')

def for_type(request):
    role = Users.objects.get(user=request.user).role
    types=ForType.objects.all()
    context={
        'role':role,
        'types':types,
    }
    return render(request,"leads/for_type.html",context)

def add_for_type(request):
    role=Users.objects.get(user=request.user).role
    if request.method == "POST":
        for_type_name   = request.POST.get("for_type_name")
        for_type_status = request.POST.get("for_type_status")
        ForType.objects.create(
            for_type_name = for_type_name,
            for_type_status = for_type_status,
        )
        messages.success(request,"Lead Type added")
        return redirect('for_type')
    context={
        'role':role
    }
    return render(request,'leads/add_for_type.html',context)

def delete_lead_type(request,id):
    ForType.objects.get(id=id).delete()
    messages.success(request,"Lead type deleted")
    return redirect('for_type')

def inactive_lead_type(request,id):
    type=ForType.objects.get(id=id)
    type.for_type_status = 'inactive'
    type.save()
    messages.success(request,"Lead type inactivated")
    return redirect('for_type')

def active_lead_type(request,id):
    type=ForType.objects.get(id=id)     
    type.for_type_status = 'active'
    type.save()
    messages.success(request,"Lead type activated")
    return redirect('for_type')

def lead_details(request,lead_id):
    role      = Users.objects.get(user=request.user).role
    lead      = Leads.objects.filter(leadid=lead_id).first()
    status    = LeadStatus.objects.filter(leadstatus_status = 'active')
    history   = LeadHistory.objects.filter(lead = lead).order_by('-id')
    reminders = Reminder.objects.filter(lead = lead).order_by('-id')
    
    if request.method == "POST":
        
        if request.POST.get("form_type") == "reminder_form":
            reminder_date = request.POST.get("reminder_date")or None
            reminder_time = request.POST.get("reminder_time")or None
            reminder_note = request.POST.get("reminder_note")or None
            Reminder.objects.create(
                lead          = lead,
                reminder_date = reminder_date,
                reminder_time = reminder_time,
                reminder_note = reminder_note,
            )
            messages.success(request,"Reminder Added Successfully")
            return redirect('lead_details',lead_id=lead.leadid)
        
        elif request.POST.get("form_type") == "lead_update":
            expected_closing = request.POST.get("expected_closing")or None
            statuses         = request.POST.get("status")
            notes            = request.POST.get("notes")
        
            status_obj = LeadStatus.objects.filter(id = statuses).first()
        
            lead.status = status_obj
            lead.save()
        
            LeadHistory.objects.create(
                lead          = lead,
                expected_date = expected_closing,
                updated_by    = EmployeeInfo.objects.filter(user=request.user).first(),
                status        = status_obj,
                notes         = notes
            )
            messages.success(request,"Lead updated successfully")
            return redirect('lead_details',lead_id=lead.leadid)

    context={
        'role'     :role,
        'lead'     :lead,
        'status'   :status,
        'history'  :history,
        'reminders':reminders,
    }
    return render(request,"leads/lead_details.html",context)


def lead_status(request):
    role     = Users.objects.get(user=request.user).role
    statuses = LeadStatus.objects.all()

    context = {
        'role'     : role,
        'statuses' : statuses,
    }
    return render(request,"leads/lead_status.html",context)

# ADD PAGE

def add_lead_status(request):
    role = Users.objects.get(user=request.user).role
    
    if request.method == "POST":
        lead_status_name  = request.POST.get("lead_status_name")
        leadstatus_status = request.POST.get("leadstatus_status")
    
        LeadStatus.objects.create(
            lead_status_name = lead_status_name,
            leadstatus_status = leadstatus_status,
        )
        messages.success(request,"Status Added Successfull")
        return redirect('lead_status')
    
    context = {
        'role':role,
    }
    return render(request,"leads/add_lead_status.html",context)


# DELETE

def delete_lead_status(request, id):
    LeadStatus.objects.get(id=id).delete()
    messages.success(request,"Status Deleted")
    return redirect('lead_status')


# ACTIVE / INACTIVE

def active_lead_status(request, id):
    
    lead = LeadStatus.objects.filter(id=id).first()
    if lead.leadstatus_status == "active":
        lead.leadstatus_status = "inactive"
    
    else :
        lead.leadstatus_status = "active"
    
    lead.save()
    messages.success(request,"Lead Status Updated Successfully")

    return redirect('lead_status')

def reminders(request):
    role = Users.objects.get(user=request.user).role
    company = UserInfo.objects.filter(user=request.user).first()
    reminders = Reminder.objects.filter(is_deleted=False).order_by('-id')
    context = {
        'role':role,
        'reminders':reminders,
        'title': 'All Reminders',
    }
    return render(request,'leads/all_reminder.html',context)

# COMPLETE REMINDER

def complete_reminder(request, id):
    reminder = Reminder.objects.filter(id=id).first()
    reminder.is_completed = True
    reminder.save()
    messages.success(request,"Reminder Completed Successfully")
    return redirect('reminders')

# DELETE REMINDER

def delete_reminder(request, id):
    reminder = Reminder.objects.filter(id=id).first()
    reminder.is_deleted = True
    reminder.save()
    messages.success(request,"Reminder Deleted Successfully")
    return redirect('reminders')
    
def today_reminders(request):
    role = Users.objects.get(user=request.user).role
    today = date.today()
    reminders = Reminder.objects.filter(reminder_date=today,is_deleted=False).order_by('reminder_time')
    context = {
        'role':role,
        'title': "Today's Reminders",
        'reminders': reminders,
    }
    return render(request,"leads/all_reminder.html",context)

def tomorrow_reminders(request):
    role = Users.objects.get(user=request.user).role
    tomorrow = date.today() + timedelta(days=1)
    reminders = Reminder.objects.filter(
        reminder_date=tomorrow,
        is_deleted=False
    ).order_by('reminder_time')
    context = {
        'role':role,
        'title': "Tomorrow Reminders",
        'reminders': reminders,
    }
    return render(
        request,
        "leads/all_reminder.html",
        context
    )