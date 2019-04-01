from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),

    #Helpers
    path('ajax/helpers', views.admin_helpers, name='get_helper'),
    path('ajax/helpers/accept', views.admin_helper_request_accept, name='accept_helper'),
    path('ajax/helpers/reject', views.admin_helper_request_reject, name='reject_helper'),
    path('ajax/helpers/revoke', views.admin_helper_revoke, name='helper_revoke'),

    #Technologies
    path('ajax/technologies', views.admin_technologies, name='get_technologies'),
    path('ajax/technologies/add', views.admin_technology_add, name='technology_add'),
    path('ajax/technologies/delete', views.admin_technology_delete, name='technology_delete'),

    #Classes
    path('ajax/classes', views.admin_classes, name='get_classes'),
    path('ajax/classes/add', views.admin_class_add, name='class_add'),
    path('ajax/classes/delete', views.admin_class_delete, name='class_delete'),

    #Titles
    path('ajax/titles', views.admin_titles, name='get_titles'),
    path('ajax/titles/add', views.admin_title_add, name='title_add'),
    path('ajax/titles/delete', views.admin_title_delete, name='title_delete'),
    
]
