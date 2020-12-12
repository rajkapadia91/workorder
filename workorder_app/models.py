from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        valid_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) <= 2:
            errors['first_name'] = "First name needs to be more than 2 characters"
        if len(postData['last_name']) <= 2:
            errors['last_name'] = "Last name needs to be more than 2 characters"
        if not valid_email.match(postData['email']): # test whether a field matches the pattern 
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email = postData['email']).exists():
            errors['unique_email'] = "Account with this email already exists!"
        if len(postData['password']) <= 6:
            errors['password'] = "Password needs to be more than 6 characters"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match!"
        if postData['secret_code'] != "Inside1" and postData['secret_code'] != "FGadmin!":
            errors['secret_code'] = "Sorry, you are not authorized to register"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    secret_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class JobName(models.Model):
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    contractor_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CarpenterForeman(models.Model):
    labor_type = models.CharField(max_length=255, default="Carpenter - Foreman")
    employee_numbers = models.CharField(max_length=255, default="0")
    regular_hours = models.CharField(max_length=255, default="0")
    over_hours = models.CharField(max_length=255,default="0")
    double_hours = models.CharField(max_length=255,default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class CarpenterJourneyamn(models.Model):
    labor_type = models.CharField(max_length=255, default="Carpenter - Journeyman")
    employee_numbers = models.CharField(max_length=255, default="0")
    regular_hours = models.CharField(max_length=255, default="0")
    over_hours = models.CharField(max_length=255,default="0")
    double_hours = models.CharField(max_length=255,default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class TaperJourneyman(models.Model):
    labor_type = models.CharField(max_length=255, default="Taper - Journeyman")
    employee_numbers = models.CharField(max_length=255, default="0")
    regular_hours = models.CharField(max_length=255, default="0")
    over_hours = models.CharField(max_length=255,default="0")
    double_hours = models.CharField(max_length=255,default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class TaperForeman(models.Model):
    labor_type = models.CharField(max_length=255, default="Taper - Foreman")
    employee_numbers = models.CharField(max_length=255, default="0")
    regular_hours = models.CharField(max_length=255, default="0")
    over_hours = models.CharField(max_length=255,default="0")
    double_hours = models.CharField(max_length=255,default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class Laborer(models.Model):
    labor_type = models.CharField(max_length=255, default="Laborer")
    employee_numbers = models.CharField(max_length=255, default="0")
    regular_hours = models.CharField(max_length=255, default="0")
    over_hours = models.CharField(max_length=255,default="0")
    double_hours = models.CharField(max_length=255,default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class Supervisor(models.Model):
    labor_type = models.CharField(max_length=255, default="Supervisor")
    employee_numbers = models.CharField(max_length=255, default="0")
    regular_hours = models.CharField(max_length=255, default="0")
    over_hours = models.CharField(max_length=255,default="0")
    double_hours = models.CharField(max_length=255,default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
 
class WorkOrder(models.Model):
    location = models.CharField(max_length=255)
    work_performed = models.TextField()
    signature_1 = models.TextField()
    signator_1 = models.CharField(max_length=255)
    signature_2 = models.TextField()
    signator_2 = models.CharField(max_length=255)
    jobname = models.ForeignKey(JobName, related_name="workorders", on_delete=models.CASCADE)
    carpenterforeman = models.ForeignKey(CarpenterForeman, related_name="workorders", on_delete=models.CASCADE)
    carpenterjourneyamn = models.ForeignKey(CarpenterJourneyamn, related_name="workorders", on_delete=models.CASCADE)
    taperjourneyman = models.ForeignKey(TaperJourneyman, related_name="workorders", on_delete=models.CASCADE)
    taperforeman = models.ForeignKey(TaperForeman, related_name="workorders", on_delete=models.CASCADE)
    laborer = models.ForeignKey(Laborer, related_name="workorders", on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, related_name="workorders", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='workorders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Material(models.Model):
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()
    workorder = models.ForeignKey(WorkOrder, related_name="materials", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class OtherMaterial(models.Model):
    other_name = models.CharField(max_length=255)
    other_quantity = models.IntegerField()
    workorder = models.OneToOneField(WorkOrder, related_name="othermaterial", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





