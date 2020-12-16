from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    if 'user_id' in request.session:
        return redirect('/createorder')
    else:
        return render(request, 'home.html')

def logout(request):
    list(messages.get_messages(request))
    request.session.flush()
    request.session.clear()
    return redirect('/')

def login(request):
    if request.method == 'POST':
        logged_user = User.objects.filter(email = request.POST['logged_email'])
        if logged_user:
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['logged_password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_fname'] = logged_user.first_name
                request.session['user_lname'] = logged_user.last_name
                request.session['secret_code'] = logged_user.secret_code
                return redirect('/createorder')
            else:
                request.session['failed_login'] = "Your credentials don't match. Please try again!"
                return redirect('/')
        else:
            request.session['failed_login'] = "Your credentials don't match. Please try again!"
            return redirect('/')
    else:
        request.session['failed_login'] = "Your credentials don't match. Please try again!"
        return redirect('/')


def create_account(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        else:
            orignal_password = request.POST['password']
            encrypted_password = bcrypt.hashpw(orignal_password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(first_name = request.POST['first_name'], last_name= request.POST['last_name'], email = request.POST['email'], password= encrypted_password, secret_code=request.POST['secret_code'])
            request.session['user_id'] = new_user.id
            request.session['user_fname'] = new_user.first_name
            request.session['user_lname'] = new_user.last_name
            request.session['secret_code'] = new_user.secret_code
            return redirect('/createorder')
    else:
        return redirect ('/')
   
def createorder(request):
    if 'user_id' in request.session:
        context = {
            'all_materials': Material.objects.all(),
            'all_jobs' : JobName.objects.all()
        }
        return render(request, 'createorder.html', context)
    else:
        return redirect('/')

def jobname(request):
    if request.session['secret_code'] == "FGadmin!" :
        print("Hey this is francesca!")
        context = {
            'all_jobs' : JobName.objects.all()
        }
        return render(request, 'jobname.html', context)
    else:
        return redirect('/')

def create_job(request):
    if request.method == 'POST':
        new_job = JobName.objects.create(name = request.POST['job_name'], contractor_name = request.POST['contractor_name'], street = request.POST['street'], city= request.POST['city'], state= request.POST['state'], zip_code = request.POST['zipcode'])
        return redirect('/jobname')
    else:
        return redirect('/jobname')

def delete_job(request, job_id):
    JobName.objects.get(id=job_id).delete()
    return redirect('/jobname')

def create_order(request):
    if request.method == 'POST':
        print('Welcome, you are trying to create a work order!')
        user_creating_order = User.objects.get(id=request.session['user_id'])
        print(user_creating_order)
        job_id_selected = JobName.objects.get(id=request.POST['contractor'])
        new_order = WorkOrder.objects.create(
            location=request.POST['location'],
            date_work_performed = request.POST['date_work_performed'],
            work_performed=request.POST['work_performed'],
            signature_1=request.POST['signature_1'],
            signator_1=request.POST['signator_1'], 
            signature_2=request.POST['signature_2'],
            signator_2=request.POST['signator_2'], 
            jobname=job_id_selected, 
            user=User.objects.get(id=user_creating_order.id))
        mat_count = int(request.POST['material_count'])
        lab_count = int(request.POST['labor_count'])
        print(lab_count)
        for i in range(1, mat_count+1):
            new_material = Material.objects.create(product=request.POST[f"product{i}"], quantity= request.POST[f"quantity{i}"], measurement=request.POST[f"measurement{i}"], measurement_amount= request.POST[f"measurement_amount{i}"], workorder=WorkOrder.objects.get(id=new_order.id))
        for n in range(1, lab_count+1):
            new_labor = LaborType.objects.create(labor_type=request.POST[f"labor_type{n}"], labor_description=request.POST[f"labor_description{n}"], employee_numbers=request.POST[f"employee_numbers{n}"], regular_hours=request.POST[f"regular_hours{n}"], premium_hours=request.POST[f"premium_hours{n}"],double_hours=request.POST[f"double_hours{n}"], workorder=WorkOrder.objects.get(id=new_order.id))
            print(new_labor)
        new_other_material = OtherMaterial.objects.create(other_name=request.POST['other_name'], other_quantity=request.POST['other_quantity'], other_measurement=request.POST['other_measurement'], other_measurement_amount=request.POST['other_measurement_amount'],  workorder=WorkOrder.objects.get(id=new_order.id))
        return redirect (f"/workorderpreview/{new_order.id}")
    else:
        return redirect('/')

def all_work_orders(request):
    if request.session['secret_code'] == "FGadmin!":
        context = {
            'all_work_orders': WorkOrder.objects.all()
            }
        return render(request, "workorder.html", context)
    else:
        return redirect ('/')

def show_work_order(request, workorder_id):
    if request.session['secret_code'] == "FGadmin!":
        context = {
            'this_work_order' : WorkOrder.objects.get(id=workorder_id)
        }
        return render(request, 'showworkorder.html', context)
    else:
        return redirect ('/')

def workorderpreview(request, workorder_id):
    if 'user_id' in request.session:
        context = {
            'this_work_order' : WorkOrder.objects.get(id=workorder_id)
        }
        return render(request, 'workorderpreview.html', context)
    else:
        return redirect('/')


def delete_work_order(request, workorder_id):
    WorkOrder.objects.get(id=workorder_id).delete()
    return redirect ('/workorder')

def editorder(request, workorder_id):
    context = {
        'edit_this_order': WorkOrder.objects.get(id=workorder_id),
        'all_jobs' : JobName.objects.all(),
        'all_materials': Material.objects.all()

    }
    return render(request, 'editorder.html', context)

def save_edit(request, workorder_id):
    if request.method == 'POST':
        edit_this_work_order = WorkOrder.objects.get(id=workorder_id)
        edit_this_work_order.signature_1=request.POST['signature_1']
        edit_this_work_order.signator_1=request.POST['signator_1']
        edit_this_work_order.signature_2=request.POST['signature_2']
        edit_this_work_order.signator_2=request.POST['signator_2']
        edit_this_work_order.save()
        return redirect(f'/workorderpreview/{workorder_id}')
    else:
        return redirect(f'/edit/{workorder_id}')

def myworkorders(request, user_id):
    context = {
        'my_work_orders' : WorkOrder.objects.filter(user=User.objects.get(id=user_id)),
        'latest_work_order': WorkOrder.objects.filter(user=User.objects.get(id=user_id)).last(),
        }
    return render(request, 'myworkorders.html', context)

def all_users(request):
    if request.session['secret_code'] == "FGadmin!":
        context = {
            'all_user_accounts' : User.objects.all()
        }
        return render(request, 'alluseraccounts.html', context)
    else:
        return redirect('/')

def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect ('/all_users')