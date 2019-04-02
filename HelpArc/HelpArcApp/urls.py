from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Auth views
    path('auth', include('django.contrib.auth.urls')),

    path('profile', views.profile, name='profile'),
    path('askhelp/<id>', views.askhelp, name='askhelp'),
    path('completeprofile', views.completeprofile, name='completeprofile'),
    path('helpRequest/<id>', views.helpRequest, name='helpRequest'),
    path('ajax/search/', views.updateindex, name='updateIndex'),
]


