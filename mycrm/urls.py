"""
URL configuration for mycrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import login_view, dashboard,logout_view
from admen.views import *
from company.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',          login_view, name="login"),
    path('dashboard/',dashboard,  name="dashboard"),
    path('logout/',   logout_view,name="logout"),
    
    
    path('add-company/',            add_company,    name="add_company"),
    path('delete-company/<int:id>/',delete_company, name="delete_company"),
    path('edit-company/<int:id>/',  edit_company,   name="edit_company"),
    path('company-details/',        company_details,name="company_details"),
    
    
    path('add-employee/',            add_employee,    name="add_employee"),
    path('delete-employee/<int:id>/',delete_employee, name="delete_employee"),
    path('edit-employee/<int:id>/',  edit_employee,   name="edit_employee"),
    path('employee-details/',        employee_details,name="employee_details"),
    
    
    path('leads/',                         leads,               name="leads"),
    path('add-leads/',                     add_leads,           name="add_leads"),
    path('delete-lead/<int:id>',           delete_lead,         name='delete_lead'),
    path('lead-source/',                   lead_source,         name='lead_source'),
    path('add-lead-source/',               add_lead_source,     name='add_lead_source'),
    path('delete-lead-source/<int:id>',    delete_lead_source,  name='delete_lead_source'),
    path('inactive-lead-source/<int:id>/', inactive_lead_source,name='inactive_lead_source'),
    path('active-lead-source/<int:id>/',   active_lead_source,  name='active_lead_source'),
    
    path('lead-type/',                     for_type,            name='for_type'),
    path('add-for-type/',                  add_for_type,        name='add_for_type'),
    path('inactive-lead-type/<int:id>/',   inactive_lead_type,  name='inactive_lead_type'),
    path('active-lead-type/<int:id>/',     active_lead_type,    name='active_lead_type'),
    path('delete-lead-type/<int:id>/',     delete_lead_type,    name='delete_lead_type'),
    path('leads-details/<str:lead_id>/',   lead_details,        name='lead_details'),
    path('lead-status/',                   lead_status,         name='lead_status'),
    path('add-lead-status/',               add_lead_status,     name='add_lead_status'),
    path('delete-lead-status/<int:id>/',   delete_lead_status,  name='delete_lead_status'),
    path('active-lead-status/<int:id>/',   active_lead_status,  name='active_lead_status' ),   
    
    path('reminders/',                       reminders,         name='reminders' ),
    path('complete-reminder/<int:id>/',      complete_reminder, name='complete_reminder'),
    path('delete-reminder/<int:id>/',        delete_reminder,   name='delete_reminder'),

path(
    'today-reminders/',
    today_reminders,
    name='today_reminders'
),

path(
    'tomorrow-reminders/',
    tomorrow_reminders,
    name='tomorrow_reminders'
),
    
    
    path('project/',                        project,            name='project'),
    path('add-project/',                    add_project,        name='add_project'),
    path('delete-project/<str:project_id>/',delete_project,     name='delete_project'),
    path('edit-project/<str:project_id>/',  edit_project,       name='edit_project'),
    path('project-details/<str:project_id>/',project_details,   name='project_details'),

]
