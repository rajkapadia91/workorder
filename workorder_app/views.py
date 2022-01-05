import csv, io
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from datetime import datetime, date, timedelta
from email.mime.image import MIMEImage
import xlwt
import csv
from django.utils.encoding import smart_str


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
        logged_user = User.objects.filter(email = request.POST['logged_email'].lower())
        if logged_user:
            logged_user = logged_user[0]
            if logged_user.active == "Active":
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
            new_user = User.objects.create(first_name = request.POST['first_name'], last_name= request.POST['last_name'], email = request.POST['email'].lower(), password= encrypted_password, secret_code=request.POST['secret_code'], active=request.POST['active'])
            request.session['user_id'] = new_user.id
            request.session['user_fname'] = new_user.first_name
            request.session['user_lname'] = new_user.last_name
            request.session['secret_code'] = new_user.secret_code
            return redirect('/createorder')
    else:
        return redirect ('/')
   
def createorder(request):
    request.session['success'] = 0
    if 'user_id' in request.session:
        context = {
            'all_materials': Material.objects.all(),
            'all_jobs' : JobName.objects.all(),
            'all_material_names': MaterialProductDB.objects.all(),
        }
        return render(request, 'createorder.html', context)
    else:
        return redirect('/')

def allmaterials(request):
    if request.session['secret_code'] == "FGadmin!" :
        context = {
            'all_material_names': MaterialProductDB.objects.all(),
        }
        return render(request, 'allmaterials.html', context)
    else:
        return redirect('/')

def create_new_material(request):
    if request.method == 'POST' and request.session['secret_code'] == "FGadmin!":
        new_material = MaterialProductDB.objects.create(
            location=request.POST['location'],
            product_name = request.POST['product_name'],
            unit_of_measurement = request.POST['unit_of_measurement'],
            price = request.POST['price']
        )
        return redirect('/allmaterials')
    else:
        return redirect('/')

def delete_material_db(request, material_id):
    if request.session['secret_code'] == "FGadmin!" :
        MaterialProductDB.objects.get(id=material_id).delete()
        return redirect('/allmaterials')
    else:
        return redirect('/')

def deleteallmaterials(request):
    if request.session['secret_code'] == "FGadmin!" :
        all_materials = MaterialProductDB.objects.all()
        for one_material in all_materials:
            MaterialProductDB.objects.get(id=one_material.id).delete()
        return redirect('/allmaterials')
    else:
        return redirect('/')

def download_material_template(request):
    if request.session['secret_code'] == 'FGadmin!':
        # response content type

        response = HttpResponse(content_type='text/csv')
        #decide the file name
        response['Content-Disposition'] = 'attachment; filename="upload_material_template.csv"'

        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))

        #write the headers
        writer.writerow([
        smart_str(u"location"),
        smart_str(u"product_name"),
        smart_str(u"unit_of_measurement"),
        smart_str(u"price")
        ])
        # no date to get - this is just a template
        writer.writerow([
        smart_str(u"Framing"),
        smart_str(u"2 ft sheets"),
        smart_str(u"SQ FT"),
        smart_str(u"3.22")
            ])
        return response
    else:
        return redirect('/')

def download_all_material(request):
    if request.session['secret_code'] == 'FGadmin!':
        # response content type

        response = HttpResponse(content_type='text/csv')
        #decide the file name
        response['Content-Disposition'] = 'attachment; filename="materialproductlist.csv"'

        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))

        #write the headers
        writer.writerow([
            smart_str(u"location"),
            smart_str(u"product_name"),
            smart_str(u"unit_of_measurement"),
            smart_str(u"price")
        ])
        #get data from database or from text file....
        materials = MaterialProductDB.objects.all()
        for one_material in materials:
            writer.writerow([
                smart_str(one_material.location),
                smart_str(one_material.product_name),
                smart_str(one_material.unit_of_measurement),
                smart_str(one_material.price)
                   ])
        return response
    else:
        return redirect('/')

def upload_material(request):
    data = MaterialProductDB.objects.all()
    prompt = {
        'order': 'Order of the CSV should be full_name, union, position',
        'profiles': data
        }
    if request.method == "GET":
        return redirect('/')
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=','):
            created = MaterialProductDB.objects.update_or_create(
            location=column[0],
            product_name=column[1],
            unit_of_measurement=column[2],
            price=column[3], 
        )
    return redirect('/allmaterials')

def jobname(request):
    if request.session['secret_code'] == "FGadmin!" :
        all_jobs = JobName.objects.all()
        contractor_names = []
        for i in range(0, len(all_jobs), 1):
            contractor_names.append(all_jobs[i].contractor_name)
        unique_contractor_names = set(contractor_names)
        context = {
            'all_jobs' : JobName.objects.all(),
            'unique_contractor_names': unique_contractor_names
        }
        return render(request, 'jobname.html', context)
    else:
        return redirect('/')

def create_job(request):
    if request.method == 'POST':
        gc_name = request.POST['contractor_name']
        if request.POST['contractor_name'] == "" or request.POST['contractor_name'] == None or request.POST['contractor_name'] == " ":
            gc_name = request.POST['gc_dropdown']
        else:
            gc_name = request.POST['contractor_name']
        new_job = JobName.objects.create(name = request.POST['job_name'], 
        contractor_name = gc_name, 
        gc_street = request.POST['gc_street'], 
        gc_city_state_zip = request.POST['gc_city_state_zip'], 
        gc_phone = request.POST['gc_phone'], 
        street = request.POST['street'], 
        city= request.POST['city'], 
        state= request.POST['state'], 
        zip_code = request.POST['zipcode'])
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
        invoice_dummy_date = date.today().strftime("%Y-%m-%d")
        new_order = WorkOrder.objects.create(
            invoice_date = invoice_dummy_date,
            invoice_number = "1111",
            request_for_pricing = request.POST['request_for_pricing'],
            location=request.POST['location'],
            date_work_performed = request.POST['date_work_performed'],
            work_performed=request.POST['work_performed'],
            priced = request.POST['priced'],
            signature_1=request.POST['signature_1'],
            signator_1=request.POST['signator_1'],
            general_contractor_email=request.POST['general_contractor_email'],
            signature_2=request.POST['signature_2'],
            signator_2=request.POST['signator_2'], 
            jobname=job_id_selected, 
            subtotal_material_cost = 0,
            subtotal_other_material_cost = 0,
            material_cost_combined = 0,
            labor_cost_combined = 0,
            total_invoice_amount = 0,
            overhead_profit = 0,
            memo = "",
            user=User.objects.get(id=user_creating_order.id))
        mat_count = int(request.POST['material_count'])
        lab_count = int(request.POST['labor_count'])
        other_mat_count = int(request.POST['other_material_count'])
        print(lab_count)
        for i in range(1, mat_count+1):
            measurement_amount_entered = 1
            prod_material = ""
            material_post = ""
            material_price = 0.0
            quantity = 0.0
            if request.POST[f"measurement_amount{i}"] == "" or request.POST[f"measurement_amount{i}"] == 0:
                measurement_amount_entered = 1
            else:
                measurement_amount_entered = request.POST[f"measurement_amount{i}"]
            if request.POST[f"product{i}"] == "" or request.POST[f"product{i}"] == " " or request.POST[f"product{i}"] == '':
                prod_material = ""
            else:
                prod_material = request.POST[f"product{i}"]
            if request.POST[f"product{i}"] == "" or request.POST[f"product{i}"] == " " or request.POST[f"product{i}"] == '':
                material_post =  ""
            else:
                material_post = prod_material.split('|')[0]
            if request.POST[f"product{i}"] == "" or request.POST[f"product{i}"] == " " or request.POST[f"product{i}"] == '':
                material_price = 0.0
            else:
                material_price = prod_material.split('|')[2].strip()
            if request.POST[f"quantity{i}"] == "" or request.POST[f"quantity{i}"] == " " or request.POST[f"quantity{i}"] == 0:
                quantity = 0
            else:
                quantity = request.POST[f"quantity{i}"]
            print(material_price)
            new_material = Material.objects.create(
                product=material_post,
                per_price = round(float(material_price),2),
                quantity= quantity, 
                measurement=request.POST[f"measurement{i}"], 
                measurement_amount= measurement_amount_entered, 
                total_material_cost = round(round(float(quantity),2) * round(float(material_price),2) * round(float(measurement_amount_entered),2),2),
                workorder=WorkOrder.objects.get(id=new_order.id))
        for c in range(1, other_mat_count+1):
            new_other_material = OtherMaterial.objects.create(other_name=request.POST[f"other_name{c}"], other_quantity=request.POST[f"other_quantity{c}"], other_measurement=request.POST[f"other_measurement{c}"], other_measurement_amount=request.POST[f"other_measurement_amount{c}"], total_other_material_cost=0  ,workorder=WorkOrder.objects.get(id=new_order.id))
            print(new_other_material)
        for n in range(1, lab_count+1):
            hourly_rate_objects = LaborRate.objects.filter(job_name=job_id_selected.name, labor_type_name=request.POST[f"labor_type{n}"])
            hourly_rate_filter = 1.11
            if hourly_rate_objects:
                hourly_rate_filter = round(float(hourly_rate_objects[0].labor_hourly_rate),2)
            else:
                hourly_rate_filter = 1.11
            print(hourly_rate_filter)
            regular_hours = request.POST[f"regular_hours{n}"]
            double_hours = request.POST[f"double_hours{n}"]
            premium_hours = request.POST[f"premium_hours{n}"]
            over_hours = request.POST[f"over_hours{n}"]
            print(f'Reg: {regular_hours}, Prem: {premium_hours}, Dou: {double_hours}')
            if request.POST[f"regular_hours{n}"] == "" or request.POST[f"regular_hours{n}"] == "'" or request.POST[f"regular_hours{n}"] == '' or request.POST[f"regular_hours{n}"] is None :
                regular_hours=0
            if request.POST[f"double_hours{n}"] == "" or request.POST[f"double_hours{n}"] == "'" or request.POST[f"double_hours{n}"] == '' or request.POST[f"double_hours{n}"] is None:
                double_hours=0
            if request.POST[f"premium_hours{n}"] == "" or request.POST[f"premium_hours{n}"] == "'" or request.POST[f"premium_hours{n}"] == '' or request.POST[f"premium_hours{n}"] is None:
                premium_hours=0
            if request.POST[f"over_hours{n}"] == "" or request.POST[f"over_hours{n}"] == "'" or request.POST[f"over_hours{n}"] == '' or request.POST[f"over_hours{n}"] is None:
                over_hours=0
            total_hours = round(float(regular_hours),2)+round(float(double_hours),2)+round(float(premium_hours),2)+round(float(over_hours),2)
            new_labor = LaborType.objects.create(
            labor_type=request.POST[f"labor_type{n}"],
            labor_description=request.POST[f"labor_description{n}"],
            employee_numbers=round(float(request.POST[f"employee_numbers{n}"]),2),
            regular_hours=round(float(regular_hours),2),
            premium_hours=round(float(premium_hours),2),
            double_hours=round(float(double_hours),2),
            over_hours=round(float(over_hours),2),
            hourly_rate = round(float(hourly_rate_filter),2),
            total_hours= total_hours,
            total_labor_cost= (hourly_rate_filter*(round(float(regular_hours),2)))+(hourly_rate_filter*(round(float(double_hours),2))*2)+(hourly_rate_filter*(round(float(over_hours),2))*1.5)+(hourly_rate_filter*(round(float(premium_hours),2))*1.0),
            workorder=WorkOrder.objects.get(id=new_order.id)
            )
            print(new_labor)
        return redirect (f"/create_email/{new_order.id}")
    else:
        return redirect('/')

def create_email(request, workorder_id):
    work_order_emailed = WorkOrder.objects.get(id=workorder_id)
    email_sender = work_order_emailed.user.email
    general_contractor_email_use_send = work_order_emailed.general_contractor_email
    context = {
            'this_work_order' : WorkOrder.objects.get(id=workorder_id)
        }
    msg_html = render_to_string('create_email.html', context)
    msg = EmailMessage(subject=f"New Submission - Extra Work Order - {workorder_id} ", body=msg_html, from_email='belconcentral@gmail.com', to=['fgalioto@belconservice.com	'], cc=[email_sender,general_contractor_email_use_send, 'dzarfino@belconservice.com'])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    return redirect(f"/workorderpreview/{workorder_id}")

def all_work_orders(request):
    if request.session['secret_code'] == "FGadmin!":
        request.session['success'] = 0
        context = {
            'all_work_orders': WorkOrder.objects.all()
            }
        return render(request, "workorder.html", context)
    else:
        return redirect ('/')

def all_work_orders_not_priced(request):
    if request.session['secret_code'] == "FGadmin!":
        request.session['success'] = 0
        context = {
            'all_work_orders': WorkOrder.objects.all()
            }
        return render(request, "workordernotpriced.html", context)
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

def workorderpreviewexternal(request, workorder_id):
    context = {
            'this_work_order' : WorkOrder.objects.get(id=workorder_id)
        }
    return render(request, 'workorderpreviewexternal.html', context)


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

def invoicepreview(request, workorder_id):
    if request.session['secret_code'] == "FGadmin!" :
        context = {
            'edit_this_order': WorkOrder.objects.get(id=workorder_id),
            'all_jobs' : JobName.objects.all(),
            'all_materials': Material.objects.all(),
            'our_company_info': OurCompanyInfo.objects.filter(status="Active"),

        }
        return render(request, 'invoicepreview.html', context)
    else:
        return redirect('/')

def our_company_info(request):
    if request.session['secret_code'] == "FGadmin!" :
        context = {
            'our_company_info': OurCompanyInfo.objects.all(),
        }
        return render(request, 'our_company_info.html', context)
    else:
        return redirect('/')

def create_company_profile(request):
    if request.session['secret_code'] == "FGadmin!" and request.method == 'POST':
        new_entry = OurCompanyInfo.objects.create(
            company_name = request.POST['company_name'],
            street = request.POST['street'],
            city_state_zip = request.POST['city_state_zip'],
            phone_number = request.POST['phone_number'],
            email_address = request.POST['email_address'],
            status = request.POST['status']
        )
        return redirect('/our_company_info')
    else:
        return redirect('/')


def edit_company_profile(request, info_id):
    if request.session['secret_code'] == "FGadmin!" and request.method == 'POST':
        this_company_profile = OurCompanyInfo.objects.get(id=info_id)
        this_company_profile.company_name = request.POST['edit_company_name']
        this_company_profile.street = request.POST['edit_street']
        this_company_profile.city_state_zip = request.POST['edit_city_state_zip']
        this_company_profile.phone_number = request.POST['edit_phone_number']
        this_company_profile.email_address = request.POST['edit_email_address']
        this_company_profile.status = request.POST['edit_status']
        this_company_profile.save()
        return redirect('/our_company_info')
    else:
        return redirect('/')

def email(request, workorder_id):
    if 'user_id' in request.session:
        context = {
            'this_work_order_email' : WorkOrder.objects.get(id=workorder_id)
        }
        return render(request, 'email.html', context)
    else:
        return redirect('/')

def save_edit(request, workorder_id):
    if request.method == 'POST':
        edit_this_work_order = WorkOrder.objects.get(id=workorder_id)
        edit_this_work_order.jobname=JobName.objects.get(id=request.POST['contractor_edit'])
        edit_this_work_order.location=request.POST['location_edit']
        edit_this_work_order.request_for_pricing=request.POST['request_for_pricing_edit']
        edit_this_work_order.date_work_performed=request.POST['date_work_performed_edit']
        edit_this_work_order.work_performed=request.POST['work_performed_edit']
        edit_this_work_order.priced=request.POST['priced_edit']
        edit_this_work_order.signature_1=request.POST['signature_1']
        edit_this_work_order.signator_1=request.POST['signator_1']
        edit_this_work_order.general_contractor_email=request.POST['general_contractor_email_edit']
        edit_this_work_order.signature_2=request.POST['signature_2']
        edit_this_work_order.signator_2=request.POST['signator_2']
        edit_this_work_order.save()
        creator_name = edit_this_work_order.user.first_name
        context  = {
            'this_work_order_email': WorkOrder.objects.get(id=workorder_id)
        }
        msg_html = render_to_string('email.html', context)
        this_work_order_details = WorkOrder.objects.get(id=workorder_id)
        recipient = edit_this_work_order.user.email
        gcemail = this_work_order_details.general_contractor_email
        msg = EmailMessage(subject=f"Extra Work Order - {edit_this_work_order.id} ", body=msg_html, from_email='belconcentral@gmail.com', to=['fgalioto@belconservice.com'], cc=[recipient,gcemail, 'dzarfino@belconservice.com'])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        return redirect(f'/workorderpreview/{workorder_id}')
    else:
        return redirect(f'/edit/{workorder_id}')

def myworkorders(request, user_id):
    request.session['success'] = 0
    context = {
        'my_work_orders' : WorkOrder.objects.filter(user=User.objects.get(id=user_id)),
        'latest_work_order': WorkOrder.objects.filter(user=User.objects.get(id=user_id)).last(),
        }
    return render(request, 'myworkorders.html', context)

def reset_password(request):
    context = {
        'my_profile' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'my_profile.html', context)

def save_reset_password(request):
    if request.method == 'POST':
        errors = User.objects.user_validator_2(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            print("There are errors")
            request.session['success'] = 0
            return redirect('/reset_password')
        else:
            my_user_details = User.objects.get(id=request.session['user_id'])
            my_orignal_password = request.POST['password']
            my_encrypted_password = bcrypt.hashpw(my_orignal_password.encode(), bcrypt.gensalt()).decode()
            my_user_details.first_name = request.POST['first_name']
            my_user_details.last_name = request.POST['last_name']
            my_user_details.email = request.POST['email'].lower()
            my_user_details.password = my_encrypted_password
            my_user_details.secret_code = request.POST['secret_code']
            my_user_details.save()
            success = "Password has been successfully changed!"
            request.session['success'] = success
            return redirect('/reset_password')
    else:
        print("Not a post request")
        return redirect('/reset_password')

def all_users(request):
    request.session['success'] = 0
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

def edit_user(request, user_id):
    context = {
        'this_user' : User.objects.get(id=user_id)
    }
    return render(request, 'this_user.html', context) 
    

def save_job_edit(request, job_id):
    if request.method == 'POST':
        edit_this_job = JobName.objects.get(id=job_id)
        edit_this_job.name = request.POST['job_name_edit']
        edit_this_job.contractor_name = request.POST['contractor_name_edit']
        edit_this_job.gc_street = request.POST['gc_street_edit']
        edit_this_job.gc_city_state_zip = request.POST['gc_city_state_zip_edit']
        edit_this_job.gc_phone = request.POST['gc_phone_edit']
        edit_this_job.street = request.POST['street_edit']
        edit_this_job.city = request.POST['city_edit']
        edit_this_job.state = request.POST['state_edit']
        edit_this_job.zip_code = request.POST['zipcode_edit']
        edit_this_job.save()
        return redirect('/jobname')
    else:
        return redirect('/jobname')

def save_user(request, user_id):
    if request.method == 'POST':
        errors = User.objects.user_validator_2(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            print("There are errors")
            request.session['success'] = 0
            return redirect(f'/edit_user/{user_id}')
        else:
            save_edit_user = User.objects.get(id=user_id)
            orignal_password = request.POST['password']
            encrypted_password = bcrypt.hashpw(orignal_password.encode(), bcrypt.gensalt()).decode()
            save_edit_user.first_name = request.POST['first_name']
            save_edit_user.last_name = request.POST['last_name']
            save_edit_user.email = request.POST['email'].lower()
            save_edit_user.password = encrypted_password
            save_edit_user.secret_code = request.POST['secret_code']
            save_edit_user.save()
            success = "Password has been successfully changed!"
            request.session['success'] = success
            return redirect(f'/edit_user/{user_id}')
    else:
        print("Not a post request")
        return redirect(f'/edit_user/{user_id}')

def save_edit_here(request, workorder_id):
    if request.method == 'POST':
        edit_this_work_order_here = WorkOrder.objects.get(id=workorder_id)
        edit_this_work_order_here.priced=request.POST['priced_edit']
        edit_this_work_order_here.save()
        return redirect('/workorder')
    else:
        return redirect('/workorder')

def active_deactive(request, user_id):
    save_edit_user = User.objects.get(id=user_id)
    save_edit_user.active = request.POST['active_edit']
    save_edit_user.save()
    return redirect ('/all_users')

def save_invoice(request,workorder_id):
    if request.method == 'POST' and request.session['secret_code'] == "FGadmin!":
        this_invoice = WorkOrder.objects.get(id=workorder_id)
        this_invoice.invoice_date = request.POST['invoice_date']
        this_invoice.invoice_number = request.POST['invoice_number']
        mat_ids = []
        other_mat_ids = []
        labor_ids = []
        subtotal_material_cost = 0
        subtotal_other_material_cost = 0
        labor_cost_combined = 0
        reg_hours = 0
        prem_hours = 0
        double_hours = 0
        over_hours = 0
        overhead_profit = round(float(request.POST['overhead_profit']),2)
        mat_filtered = Material.objects.filter(workorder=WorkOrder.objects.get(id=workorder_id))
        for mat in mat_filtered:
            if mat.product != "":
                mat_ids.append(mat.id)  
        other_mat_filtered = OtherMaterial.objects.filter(workorder=WorkOrder.objects.get(id=workorder_id))
        for other_mat in other_mat_filtered:
            if other_mat.other_name != "":
                other_mat_ids.append(other_mat.id)  
        labor_filtered = LaborType.objects.filter(workorder=WorkOrder.objects.get(id=workorder_id))
        for labor in labor_filtered:
            if labor.labor_type != "":
                labor_ids.append(labor.id)  
        for i in range(0, len(mat_ids), 1):
            material_id = mat_ids[i]
            print(material_id)
            edit_this_material = Material.objects.get(id=material_id)
            edit_this_material.quantity = request.POST[f'quantity{material_id}']
            if edit_this_material.measurement == "EA" or edit_this_material.measurement == "Box(s)":
                edit_this_material.measurement_amount = 1
            else:
                edit_this_material.measurement_amount = request.POST[f'measurement_amount{material_id}']
            edit_this_material.total_material_cost = request.POST[f'total_material_cost{material_id}']
            edit_this_material.per_price = round(float(request.POST[f'per_price{material_id}']),2)
            subtotal_material_cost = subtotal_material_cost + round(float(request.POST[f'total_material_cost{material_id}']),2)
            edit_this_material.save()
        for x in range(0, len(other_mat_ids), 1):
            other_material_id = other_mat_ids[x]
            edit_other_material = OtherMaterial.objects.get(id=other_material_id)
            edit_other_material.other_quantity = request.POST[f'other_quantity{other_material_id}']
            edit_other_material.other_measurement_amount = request.POST[f'other_measurement_amount{other_material_id}']
            edit_other_material.total_other_material_cost = request.POST[f'total_other_material_cost{other_material_id}']
            subtotal_other_material_cost = subtotal_other_material_cost + round(float(request.POST[f'total_other_material_cost{other_material_id}']),2)
            edit_other_material.save()
        for y in range(0, len(labor_ids), 1):
            labor_id = labor_ids[y]
            edit_labor = LaborType.objects.get(id=labor_id)
            reg_hours = round(float(edit_labor.regular_hours),2)
            prem_hours = round(float(edit_labor.premium_hours),2)
            double_hours = round(float(edit_labor.double_hours),2)
            over_hours = round(float(edit_labor.over_hours),2)
            total_labor_hours = reg_hours+prem_hours+double_hours+over_hours
            edit_labor.employee_numbers = request.POST[f'employee_numbers{labor_id}']
            edit_labor.hourly_rate = round(float(request.POST[f'hourly_rate{labor_id}']),2)
            if round(float(request.POST[f'total_hours{labor_id}']),2) != round(float(total_labor_hours),2):
                edit_labor.total_hours = request.POST[f'total_hours{labor_id}']
            else:
                edit_labor.total_hours = round(float(reg_hours+prem_hours+double_hours),2)
            edit_labor.total_labor_cost = request.POST[f'total_labor_cost{labor_id}']
            labor_cost_combined = labor_cost_combined + round(float(request.POST[f'total_labor_cost{labor_id}']),2)
            edit_labor.save()
        this_invoice.material_cost_combined = round(float(subtotal_material_cost + subtotal_other_material_cost),2)
        this_invoice.overhead_profit = overhead_profit
        this_invoice.labor_cost_combined = labor_cost_combined
        this_invoice.total_invoice_amount = round(float(subtotal_material_cost + subtotal_other_material_cost + labor_cost_combined + overhead_profit),2)
        this_invoice.memo = request.POST['memo']
        this_invoice.save()
        return redirect(f'/invoicepreview/{workorder_id}')
    else:
        return redirect('/')

def finalinvoice(request, workorder_id):
    if request.session['secret_code'] == "FGadmin!" :
            context = {
                'edit_this_order': WorkOrder.objects.get(id=workorder_id),
                'this_work_order' : WorkOrder.objects.get(id=workorder_id),
                'all_jobs' : JobName.objects.all(),
                'all_materials': Material.objects.all(),
                 'our_company_info': OurCompanyInfo.objects.filter(status="Active"),

            }
            return render(request, 'finalinvoice.html', context)
    else:
        return redirect('/')

def laborrates(request):
    if request.session['secret_code'] == "FGadmin!":
        context = {
            'all_labor_rates' : LaborRate.objects.all(),
            'all_jobs' : JobName.objects.all(),
        }
        return render(request, 'laborrates.html', context)
    else:
        return redirect('/')

def create_labor_rate(request):
    if request.method == 'POST' and request.session['secret_code'] == "FGadmin!":
        new_labor_rate = LaborRate.objects.create(
            labor_type_name = request.POST['labor_type_name'],
            job_name = request.POST['job_name'],
            labor_hourly_rate = round(float(request.POST['labor_hourly_rate']),2)
        )
        return redirect('/laborrates')
    else:
        return redirect('/')

def delete_labor_rate(request, labor_rate_id):
    if request.session['secret_code'] == "FGadmin!":
        LaborRate.objects.get(id=labor_rate_id).delete()
        return redirect('/laborrates')
    else:
        return redirect('/')

def upload_labor_rate(request):
    if request.session['secret_code'] == 'FGadmin!':
        data = LaborRate.objects.all()
        prompt = {
            'order': 'Order of the CSV should be full_name, union, position',
            'profiles': data
            }
        if request.method == "GET":
            return redirect('/')
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):
                created = LaborRate.objects.update_or_create(
                labor_type_name=column[0],
                job_name=column[1],
                labor_hourly_rate=column[2]
            )
        return redirect('/laborrates')
    else:
        return redirect('/')

def delete_all_labor_rates(request):
    if request.session['secret_code'] == "FGadmin!" :
        all_rates = LaborRate.objects.all()
        for one_rate in all_rates:
            LaborRate.objects.get(id=one_rate.id).delete()
        return redirect('/laborrates')
    else:
        return redirect('/')

def download_labor_rate_template(request):
    if request.session['secret_code'] == 'FGadmin!':
        # response content type

        response = HttpResponse(content_type='text/csv')
        #decide the file name
        response['Content-Disposition'] = 'attachment; filename="upload_labor_rate_template.csv"'

        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))

        #write the headers
        writer.writerow([
        smart_str(u"labor_type_name"),
        smart_str(u"job_name"),
        smart_str(u"labor_hourly_rate")
        ])
        # no date to get - this is just a template
        writer.writerow([
        smart_str(u"Carpenter - Foreman"),
        smart_str(u"ABCD Example"),
        smart_str(u"150.50")
            ])
        return response
    else:
        return redirect('/')

def download_all_labor_rates(request):
    if request.session['secret_code'] == 'FGadmin!':
        # response content type

        response = HttpResponse(content_type='text/csv')
        #decide the file name
        response['Content-Disposition'] = 'attachment; filename="LaborratesbyJob.csv"'

        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))

        #write the headers
        writer.writerow([
            smart_str(u"labor_type_name"),
            smart_str(u"job_name"),
            smart_str(u"labor_hourly_rate")
        ])
        #get data from database or from text file....
        laborrates = LaborRate.objects.all()
        for one_rate in laborrates:
            writer.writerow([
                smart_str(one_rate.labor_type_name),
                smart_str(one_rate.job_name),
                smart_str(one_rate.labor_hourly_rate)
                   ])
        return response
    else:
        return redirect('/')