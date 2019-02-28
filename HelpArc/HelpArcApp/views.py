from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy

def index(request):
    context = {}
    return render(request, 'HelpArcApp/index.html', context)

def profile(request):
    context = {}
    return render(request, 'HelpArcApp/profile.html', context)

def askhelp(request):
    context = {}
    return render(request, 'HelpArcApp/askhelp.html', context)

def completeprofile(request):
    context = {}
    return render(request, 'HelpArcApp/completeprofile.html', context)