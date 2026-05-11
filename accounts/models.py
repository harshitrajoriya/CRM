from django.db import models
from django.contrib.auth.models import User
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