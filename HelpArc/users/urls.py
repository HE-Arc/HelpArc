from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('ajax/helper', views.admin_helper_requests, name='get_helper'),
    path('ajax/helper/accept', views.admin_helper_request_accept, name='accept_helper'),
    path('ajax/helper/reject', views.admin_helper_request_reject, name='reject_helper'),
    path('ajax/helper/revoke', views.admin_helper_revoke, name='helper_revoke'),
    path('ajax/technologies', views.admin_technologies, name='get_technologies'),
    path('ajax/technologies/add', views.admin_technology_add, name='technology_add'),
    path('ajax/technologies/delete', views.admin_technology_delete, name='technology_delete'),
    path('ajax/classes', views.admin_classes, name='get_classes'),
    path('ajax/classes/add', views.admin_class_add, name='class_add'),
    path('ajax/classes/delete', views.admin_class_delete, name='class_delete'),
    
]
