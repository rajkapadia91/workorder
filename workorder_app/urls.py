from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logout', views.logout),
    path('login', views.login),
    path('create_account', views.create_account),
    path('createorder', views.createorder),
    path('jobname', views.jobname),
    path('create_jobname', views.create_job),
    path('delete_job/<int:job_id>', views.delete_job),
    path('create_order', views.create_order),
    path('workorder', views.all_work_orders),
    path('workordernotpriced', views.all_work_orders_not_priced),
    path('myworkorders/<int:user_id>', views.myworkorders),
    path('reset_password', views.reset_password),
    path('save_reset_password', views.save_reset_password),
    path('show_work_order/<int:workorder_id>', views.show_work_order),
    path('delete/<int:workorder_id>', views.delete_work_order),
    path('workorderpreview/<int:workorder_id>', views.workorderpreview),
    path('workorderpreviewexternal/<int:workorder_id>', views.workorderpreviewexternal),
    path('edit/<int:workorder_id>', views.editorder),
    path('save_edit/<int:workorder_id>', views.save_edit),
    path('edit_job/<int:job_id>', views.save_job_edit),
    path('all_users', views.all_users),
    path('edit_user/<int:user_id>', views.edit_user),
    path('save_user/<int:user_id>', views.save_user),
    path('save_edit_here/<int:workorder_id>', views.save_edit_here),
    path('active_deactive/<int:user_id>', views.active_deactive),
    path('delete_user/<int:user_id>', views.delete_user),
    path('email/<int:workorder_id>', views.email),
    path('create_email/<int:workorder_id>', views.create_email),
    path('create_new_material', views.create_new_material),
    path('delete_material_db/<int:material_id>', views.delete_material_db),
    path('allmaterials', views.allmaterials),
    path('upload_material', views.upload_material),
    path('invoicepreview/<int:workorder_id>', views.invoicepreview),
    path('our_company_info', views.our_company_info),
    path('create_company_profile', views.create_company_profile),
    path('save_invoice/<int:workorder_id>', views.save_invoice),
    path('finalinvoice/<int:workorder_id>', views.finalinvoice),
    path('edit_company_profile/<int:info_id>', views.edit_company_profile),
    path('deleteallmaterials', views.deleteallmaterials),
    path('download_material_template', views.download_material_template),
    path('download_all_material', views.download_all_material),
    path('laborrates', views.laborrates),
    path('create_labor_rate', views.create_labor_rate),
    path('delete_labor_rate/<int:labor_rate_id>', views.delete_labor_rate),
    path('download_all_labor_rates', views.download_all_labor_rates),
    path('download_labor_rate_template', views.download_labor_rate_template),
    path('delete_all_labor_rates', views.delete_all_labor_rates),
    path('upload_labor_rate', views.upload_labor_rate),
    path('delete_specific_wo', views.delete_specific_wo),
    path('download_all_jobs', views.download_all_jobs),
    path('update_job_values', views.update_job_values)
]
