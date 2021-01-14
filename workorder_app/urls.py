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
    path('myworkorders/<int:user_id>', views.myworkorders),
    path('show_work_order/<int:workorder_id>', views.show_work_order),
    path('delete/<int:workorder_id>', views.delete_work_order),
    path('workorderpreview/<int:workorder_id>', views.workorderpreview),
    path('edit/<int:workorder_id>', views.editorder),
    path('save_edit/<int:workorder_id>', views.save_edit),
    path('edit_job/<int:job_id>', views.save_job_edit),
    path('all_users', views.all_users),
    path('edit_user/<int:user_id>', views.edit_user),
    path('save_user/<int:user_id>', views.save_user),
    path('delete_user/<int:user_id>', views.delete_user)
]
