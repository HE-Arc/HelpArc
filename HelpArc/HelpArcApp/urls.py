from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Auth views
    path('auth', include('django.contrib.auth.urls')),

    path('profile', views.profile, name='profile'),
    path('askhelp', views.askhelp, name='askhelp'),
    path('completeprofile', views.completeprofile, name='completeprofile'),
]
