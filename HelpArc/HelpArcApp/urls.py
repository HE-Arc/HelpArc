from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Auth views
    path('auth', include('django.contrib.auth.urls')),

    path('profile', views.profile, name='profile'),
    path('askhelp/<id>', views.askhelp, name='askhelp'),
    #path('completeprofile', views.completeprofile, name='completeprofile'),
    path('helpRequest/<id>', views.helpRequest, name='helpRequest'),

    path('ajax/update_profile', views.update_profile, name='profile_update'),
    path('ajax/update_account', views.update_account, name='account_update'),
    path('ajax/update_helper', views.update_helper, name='helper_update'),

]


