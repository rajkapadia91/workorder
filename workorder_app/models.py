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

    def user_validator_2(self, postData):
        errors = {}
        valid_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) <= 2:
            errors['first_name'] = "First name needs to be more than 2 characters"
        if len(postData['last_name']) <= 2:
            errors['last_name'] = "Last name needs to be more than 2 characters"
        if not valid_email.match(postData['email']): # test whether a field matches the pattern 
            errors['email'] = "Invalid email address!"
        if len(postData['password']) <= 6:
            errors['password'] = "Password needs to be more than 6 characters"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    secret_code = models.CharField(max_length=10)
    active = models.CharField(max_length=20, default="Active")
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
 
class WorkOrder(models.Model):
    location = models.CharField(max_length=255)
    date_work_performed = models.CharField(max_length=255, default="None")
    work_performed = models.TextField()
    priced = models.CharField(max_length=10, default="None")
    signature_1 = models.TextField()
    signator_1 = models.CharField(max_length=255)
    signature_2 = models.TextField()
    signator_2 = models.CharField(max_length=255)
    jobname = models.ForeignKey(JobName, related_name="workorders", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='workorders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Material(models.Model):
    product = models.CharField(max_length=255, default="None")
    quantity = models.CharField(max_length=10, default="0")
    measurement = models.CharField(max_length=20, default="None")
    measurement_amount = models.CharField(max_length=20, default="None")
    workorder = models.ForeignKey(WorkOrder, related_name="materials", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class OtherMaterial(models.Model):
    other_name = models.CharField(max_length=255, default="None")
    other_quantity = models.CharField(max_length=10, default="0")
    other_measurement = models.CharField(max_length=20, default="None")
    other_measurement_amount = models.CharField(max_length=20, default="None")
    workorder = models.ForeignKey(WorkOrder, related_name="othermaterials", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LaborType(models.Model):
    labor_type = models.CharField(max_length=255, default="None")
    labor_description = models.CharField(max_length=255, default="None")
    employee_numbers = models.CharField(max_length=255, default="0")
    regular_hours = models.CharField(max_length=255, default="0")
    premium_hours = models.CharField(max_length=255,default="0")
    double_hours = models.CharField(max_length=255,default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    workorder = models.ForeignKey(WorkOrder, related_name="labortypes", on_delete=models.CASCADE)





