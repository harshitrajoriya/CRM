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
from admen.views import add_company,delete_company,edit_company,company_details
from company.views import add_employee,delete_employee,edit_employee,employee_details
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login_view,name="login"),
    path('dashboard/',dashboard,name="dashboard"),
    path('logout/',logout_view,name="logout"),
    
    
    path('add-company/',add_company,name="add_company"),
    path('delete-company/<int:id>/',delete_company,name="delete_company"),
    path('edit-company/<int:id>/',edit_company,name="edit_company"),
    path('company-details/',company_details,name="company_details"),
    
    
    path('add-employee/',add_employee,name="add_employee"),
    path('delete-employee/<int:id>/',delete_employee,name="delete_employee"),
    path('edit-employee/<int:id>/',edit_employee,name="edit_employee"),
    path('employee-details/',employee_details,name="employee_details"),
    
]
