from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('askhelp', views.askhelp, name='askhelp'),
    path('completeprofile', views.completeprofile, name='completeprofile'),
]
