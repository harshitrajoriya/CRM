from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Users(models.Model):
    ROLE_CHOICES=[
        ('admin','Admin'),
        ('superadmin','Super Admin'),
        ('company','Company'),
        ('employee','employee'),
    ]
    user     = models.ForeignKey(User,on_delete=models.CASCADE)
    phone    = models.CharField(max_length=15,blank=True)
    role     = models.CharField(max_length=20,choices=ROLE_CHOICES)

class UserInfo(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    userid       = models.CharField(max_length=50, unique=True, blank=True)
    company_name = models.CharField(max_length=50,blank=True)
    address      = models.TextField(max_length=200,blank=True)
    gst          = models.CharField(max_length=20,blank=True)
    
    def save (self, *args, **kwargs) :
        super () . save(*args, **kwargs)
        if not self. userid:
            self. userid = f'USR-{self.id:06d}'
            UserInfo.objects.filter(pk=self.pk).update(userid=self.userid)

class EmployeeInfo(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    company      = models.ForeignKey(UserInfo,on_delete=models.CASCADE,blank=True,null=True,related_name="employees")
    employee_name= models.CharField(max_length=50,blank=True)
    address      = models.TextField(max_length=200,blank=True)
    dob          = models.CharField(max_length=20,blank=True)
    doj          = models.CharField(max_length=20,blank=True)
    salary       = models.CharField(max_length=20,blank=True)
    
    def get_userid(self):
        return self.user.userinfo.userid

class Leads(models.Model):
    company          = models.ForeignKey(UserInfo,related_name="lead", on_delete=models.CASCADE)
    leadid           = models.CharField(max_length=50, unique=True, blank=True)
    company_name     = models.CharField(blank=True, max_length=50)
    lead_name        = models.CharField(max_length=50,blank=True)
    lead_phone       = models.CharField(max_length=15,blank=True)
    lead_email       = models.EmailField(blank=True)
    from_assign_user = models.ForeignKey(EmployeeInfo,related_name="assign", on_delete=models.CASCADE)
    to_assign_user   = models.ForeignKey(EmployeeInfo,related_name="assigned", on_delete=models.CASCADE)
    lead_source      = models.ForeignKey("Leadsource",on_delete=models.CASCADE)
    for_type         = models.ForeignKey("ForType",on_delete=models.CASCADE)
    status           = models.ForeignKey("LeadStatus",on_delete=models.CASCADE)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    deleted_at       = models.DateTimeField(blank=True,null=True)
    
    def save (self, *args, **kwargs) :
        super () . save(*args, **kwargs)
        if not self. leadid:
            self. leadid = f'LEAD-{self.id:06d}'
            Leads.objects.filter(pk=self.pk).update(leadid=self.leadid)

class Leadsource(models.Model):
    STATUS_CHOICES = [
        ('active','Active'),
        ('inactive','Inactive'),
    ]
    lead_source_name = models.CharField(max_length=50)
    lead_status      = models.CharField(max_length=20,choices=STATUS_CHOICES,default='active')
    
class ForType(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive','Inactive'),
    ]
    for_type_name   = models.CharField(max_length=50)
    for_type_status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='active')
    
class Project(models.Model):
    PRIORITY_CHOICES = [
        ('high','High'),
        ('medium','Medium'),
        ('low','Low'),
    ]
    STATUS_CHOICES = [
        ('not started','Not Started'),
        ('in progress','In progress'),
        ('on hold','On Hold'),
        ('completed','Completed'),
    ]
    company             = models.ForeignKey(UserInfo,related_name="project",on_delete=models.CASCADE)
    project_id          = models.CharField(max_length=20,unique=True,blank=True,null=True)
    project_name        = models.CharField(max_length=50,blank=True)
    project_description = models.TextField(blank=True)
    client_name         = models.CharField(max_length=50,blank=True)
    start_date          = models.DateField(blank=True,null=True)
    end_date            = models.DateField(blank=True,null=True)
    assign_to           = models.ForeignKey(EmployeeInfo,related_name="to",on_delete=models.CASCADE)
    priority            = models.CharField(choices=PRIORITY_CHOICES, max_length=20)
    status              = models.CharField(max_length=20,choices=STATUS_CHOICES,default="not started")
    
    def save (self, *args, **kwargs) :
        super () . save(*args, **kwargs)
        if not self. project_id:
            self. project_id = f'PJ-{self.id:05d}'
            Project.objects.filter(pk=self.pk).update(project_id=self.project_id)

class LeadStatus(models.Model):
    STATUS_CHOICES = [
        ('active','Active'),
        ('inactive','Inactive'),
    ]
    lead_status_name = models.CharField(max_length=50)
    leadstatus_status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='active')
    
class LeadHistory(models.Model):
    lead = models.ForeignKey(Leads,related_name="history",on_delete=models.CASCADE)
    updated_by = models.ForeignKey(EmployeeInfo,on_delete=models.CASCADE)
    status = models.ForeignKey(LeadStatus,on_delete=models.CASCADE)
    expected_date = models.DateField(blank=True,null=True)  
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
